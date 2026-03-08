import asyncio
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from uvicorn.config import Config
from uvicorn.server import Server

from api.item_router import create_items_router
from api.location_router import create_locations_router
from api.tag_router import create_tags_router
from database.database_manager import DatabaseManager
from common_constants import FILE_STORAGE_PATH
from repositories.location_repository import LocationRepository
from repositories.tag_repository import TagRepository
from services.file_storage_service import FileStorageService
from services.item_service import ItemService
from services.location_service import LocationService
from services.tag_service import TagService
from fastapi.responses import FileResponse

FRONTEND_DIST = "./dist"


class Webserver:
    """
    Webserver for serving the FastAPI and the frontend in production.
    Has as deployment mode to only serve the frontend in production as it is directly served by vite in development.
    """

    def __init__(self, db: DatabaseManager):
        self.app = FastAPI()
        # Init repositories and services:
        project_repository = LocationRepository(db)
        tag_repository = TagRepository(db)
        project_service = LocationService(project_repository)
        tag_service = TagService(tag_repository)
        item_service = ItemService(db)
        if not os.path.exists(FILE_STORAGE_PATH):
            os.makedirs(FILE_STORAGE_PATH)
        self.app.include_router(create_locations_router(project_service), prefix="/api/locations")
        self.app.include_router(create_tags_router(tag_service), prefix="/api/tags")
        self.app.include_router(create_items_router(item_service, FileStorageService()), prefix="/api/items")

        self.app.mount(
            "/data/files",
            StaticFiles(directory=FILE_STORAGE_PATH),
            name="data",
        )

        if os.getenv("DEPLOYMENT_MODE") == "docker":
            self.app.mount(
                "/assets",
                StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")),
                name="assets",
            )
            async def serve_spa(full_path: str):
                file = os.path.join(FRONTEND_DIST, full_path)
                if os.path.isfile(file):
                    return FileResponse(file)
                return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))

            self.app.add_api_route("/{full_path:path}", serve_spa, methods=["GET"])

    async def run_server(self):
        """
        Starts the api server.
        """
        config = Config(self.app, host="0.0.0.0", port=3000, log_config=None)
        server = Server(config)
        _ = asyncio.create_task(server.serve())
