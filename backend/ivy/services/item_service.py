"""
Service layer for managing items.
"""
from database.db import AsyncSessionLocal
from models.db_models.item import Item
from models.db_models.item_attachment_mappings import ItemAttachment
from models.db_models.tag import Tag
from models.item_model import ItemModel, ItemResponseModel
from services import file_storage_service
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload


async def create_item(item_model: ItemModel) -> ItemModel:
    """
    Creates a new item in the database based on the provided ItemModel. Also handle simage attachments and tags.
    :param item_model: The ItemModel instance containing the details of the item to create.
    :return: The created ItemModel instance with the assigned ID and finalized image/attachment paths
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            item = Item(**item_model.model_dump(exclude={"tags", "tag_ids", "attachments", "image", "location"}))
            session.add(item)
            # flush to get the item ID
            await session.flush()
            item_model.id = item.id

            if item_model.image is not None:
                image_path = file_storage_service.finalize_image_upload(item_model.image, item.id)
                item.image = image_path
                item_model.image = image_path
            final_paths = file_storage_service.finalize_upload(item_model.attachments, item.id)
            session.add_all([ItemAttachment(item_id=item.id, attachment_path=path) for path in final_paths])
            item_model.attachments = final_paths

            if item_model.tags:
                result = await session.execute(select(Tag).where(Tag.id.in_([t.id for t in item_model.tags])))
                tags = result.scalars().all()
                item_model.tags = list(tags)
        return item_model

async def delete_item(item_id: int):
    """
    Deletes an item by its ID.
    :param item_id: The ID of the item to delete.
    :raises ValueError: If the item ID does not exist.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(delete(Item).where(Item.id == item_id))
        if result.rowcount == 0:
            raise ValueError(f"Item with ID '{item_id}' does not exist.")
        await session.commit()
    file_storage_service.delete_files_for_item(item_id)

async def list_items() -> list[ItemResponseModel]:
    """
    Lists all items with their associated tags, location, and attachments.
    :return: A list of ItemResponseModel instances.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Item).options(
                selectinload(Item.tags),
                selectinload(Item.attachments),
                selectinload(Item.location)
            )
        )
        items = result.scalars().all()
        return [ItemResponseModel.model_validate(item.__dict__) for item in items]
