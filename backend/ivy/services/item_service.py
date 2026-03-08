from database.database_manager import DatabaseManager
from models.item_model import ItemModel, ItemResponseModel
from repositories.item_repository import ItemRepository
from repositories.location_repository import LocationRepository
from repositories.tag_repository import TagRepository
from services.file_storage_service import FileStorageService


class ItemService:
    """
    Service for managing items.
    """

    def __init__(self, db: DatabaseManager):
        self.repo = ItemRepository(db)
        self._tag_repo = TagRepository(db)
        self._location_repo = LocationRepository(db)
        self.db_manager = db

    async def create(self, item_model: ItemModel, storage_service: FileStorageService) -> ItemModel:
        """
        Creates a new item and assigns tags and attachments.
        :param item_model: The ItemModel instance containing item details.
        :param storage_service: The FileStorageService instance for handling file uploads.
        :return: The created ItemModel instance with assigned ID and finalized attachment paths.
        """
        # This is a bit different than other services because we need to handle the related entities as well
        # We do this in a transaction to ensure nothing gets created if one part fails
        # NOTE: Im still not quite happy with how this works and how it kind of breaks the service/repo pattern.
        # Might need to revisit this down the line
        async with self.db_manager.transaction() as db:
            item_id = await self.repo.create(db, item_model)
            item_model.id = item_id
            if item_model.image is not None:
                image_path = storage_service.finalize_image_upload(item_model.image, item_model.id)
                item_model.image = image_path
                await self.repo.update_image_path(db, item_model.id, image_path)
            final_paths = storage_service.finalize_upload(item_model.attachments, item_model.id)
            item_model.attachments = final_paths
            await self.repo.assign_tags(db, item_model)
            await self.repo.add_attachments(db, item_model)
        return item_model

    async def list(self) -> list[ItemResponseModel]:
        """
        Lists all items with their associated tags, location, and attachments.
        :return: A list of ItemResponseModel instances.
        """
        # TODO: I definitely need to rework this later. For the first prototype itll work.
        # NOTE: maybe i can move some of the logic into their own funcs but im not yet sure where i would put them (repo? service?)
        item_models = await self.repo.list_all()
        for item in item_models:
            tag_ids = await self.repo.get_assigned_tag_ids(item.id)
            item.tag_ids = tag_ids
        tag_ids = []
        locations = []
        for item in item_models:
            for tag_id in item.tag_ids:
                if tag_id not in tag_ids:
                    tag_ids.append(tag_id)
            if item.location_id and item.location_id not in [loc.id for loc in locations]:
                location = await self._location_repo.get_location(item.location_id)
                if location and locations not in locations:
                    locations.append(location)
        tags = await self._tag_repo.get_tags_by_ids(tag_ids)

        item_response_models = []

        # map back to model - dont like the [""] access. feels like im fighting against pydantic
        for item in item_models:
            item_data = item.model_dump()
            item_tags = [tag for tag in tags if tag.id in item.tag_ids]
            item_data["tags"] = item_tags
            item_data["location"] = next((loc for loc in locations if loc.id == item.location_id), None)
            item_data["attachments"] = await self.repo.get_attachments(item.id)
            item_response_models.append(ItemResponseModel.model_validate(item_data))


        return item_response_models
