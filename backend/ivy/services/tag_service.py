"""
Service layer for managing tags.
"""
from database.db import AsyncSessionLocal
from models.db_models.item_tag import item_tag_mappings
from models.db_models.tag import Tag
from models.tag_model import TagModel, TagUsageModel
from utils.helper import generate_random_hex_color
from sqlalchemy.exc import IntegrityError
from sqlalchemy import  select, delete, func, distinct

async def create_tag(tag_name: str, tag_color: str) -> int:
    tag_name = tag_name.strip()
    if tag_name == "":
        raise ValueError("Tag name cannot be empty.")

    tag_color = tag_color.strip() or generate_random_hex_color()
    async with AsyncSessionLocal() as session:
        tag = Tag(name=tag_name, color=tag_color)
        session.add(tag)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise ValueError(f"Tag '{tag_name}' already exists.")
        await session.refresh(tag)
        return tag.id

async def update_tag(tag_id: int, tag_name: str, tag_color: str):
    """
    Updates the name and color for an existing tag with the given ID.
    If the color is empty, a random hex color will be generated.
    :param tag_id: The ID of the tag to update.
    :param tag_name: The new name for the tag.
    :param tag_color: The new color for the tag. If empty, a random color will be generated.
    :raises ValueError: If the tag ID does not exist or if the tag name is empty.
    """
    if tag_name.strip() == "":
        raise ValueError("Tag name cannot be empty.")
    if tag_color.strip() == "":
        tag_color = generate_random_hex_color()
    async with AsyncSessionLocal() as session:
        # Fetch the location by ID
        result = await session.execute(
            select(Tag).where(Tag.id == tag_id)
        )
        existing_tag = result.scalars().first()

        if existing_tag is None:
            raise ValueError(f"Tag with ID '{existing_tag.id}' does not exist.")

        # Update the location name
        existing_tag.name = tag_name.strip()
        existing_tag.color = tag_color.strip()
        await session.commit()

async def delete_tag(tag_id: int):
    """
    Deletes the tag with the given ID and unlinks it from any associated items.
    :param tag_id: The ID of the tag to delete.
    :raises ValueError: If the tag ID does not exist.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(delete(Tag).where(Tag.id == tag_id))
        if result.rowcount == 0:
            raise ValueError(f"Tag with ID '{tag_id}' does not exist.")
        await session.commit()
    # tag unlinking is taken care of by the foreign key constraint with ON DELETE CASCADE in the item_tag_mappings table

async def list_tags_usage() -> TagUsageModel:
    """
    Lists the usage statistics of tags (how many are used, unused, ...)
    Currently only lists used vs unused but can be extended in the future with stuff like most used tags, least used tags, etc.
    :return: TagUsageModel containing usage statistics.
    """
    async with AsyncSessionLocal() as session:
        used_tags_result = await session.execute(select(func.count(distinct(item_tag_mappings.c.tag_id))))
        used_tags = used_tags_result.scalar() or 0

        total_tags_result = await session.execute(select(func.count(Tag.id)))
        total_tags = total_tags_result.scalar() or 0

        return TagUsageModel(used=used_tags, unused=total_tags - used_tags)

async def list_tags() -> list[TagModel]:
    """
    Lists all tags.
    :return: A list of TagModel instances.
    """
    async with AsyncSessionLocal() as session:
        curr =  (await session.scalars(select(Tag))).all()
        return [TagModel.model_validate(t) for t in curr]
