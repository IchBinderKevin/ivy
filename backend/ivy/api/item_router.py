import json
import os
import uuid

from models.attachment_model import AttachmentModel
from models.item_model import ItemModel, ItemResponseModel
from services.file_storage_service import FileStorageService
from services.item_service import ItemService
from fastapi import APIRouter, status, HTTPException, Response, Form, UploadFile, File

from utils.validation_util import validate_safe


def create_items_router(service: ItemService, storage_service: FileStorageService):
    """
    Creates the router for item related endpoints.
    """
    router = APIRouter()

    @router.post("/create")
    async def create_item(item = Form(...), image: UploadFile | None = File(default=None),
                          attachments: list[UploadFile] = File(default=[])):
        """
        Creates a new item with the provided details and attachments.
        :param item: The form data for item creation.
        :param image: An optional image file to be associated with the item.
        :param attachments: A list of files to be attached to the item.
        :return: A response indicating the success or failure of the item
        """
        try:
            item = json.loads(item)
            item = ItemModel.model_validate(item)
            if image is not None: # needed because at this point item.image is always none
                item.image = storage_service.stage_image_upload(image)
            item.attachments = storage_service.stage_uploads(attachments)
            await service.create(item, storage_service)

            return Response(status_code=status.HTTP_201_CREATED)
        except ValueError as e:
            raise HTTPException(400, str(e))

    @router.delete("/delete/{item_id}")
    async def delete_item(item_id: int):
        """
        Deletes a item by its ID.
        :param item_id: The ID of the item to delete.
        """
        try:
            await service.delete(item_id, storage_service)
            return Response(status_code=status.HTTP_200_OK)
        except ValueError as e:
            raise HTTPException(400, str(e))


    @router.get("/list")
    async def list_items() -> list[ItemResponseModel]:
        """
        Lists all items with their associated tags, location, and attachments.
         :return: A list of ItemResponseModel instances.
        """
        items = await service.list()
        return items

    return router
