"""
Service layer for managing locations.
"""
from database.db import AsyncSessionLocal
from models.db_models.location import Location
from models.location_model import LocationModel
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError


async def create_location(location_name: str):
    """
    Creates a new location with the given name.
    :param location_name: The name of the location to create.
    :raises ValueError: If the location name is empty or if a location with the same name already exists.
    """
    if location_name.strip() == "":
        raise ValueError("Location name cannot be empty.")

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Location).where(Location.name == location_name.strip()))
        if result.scalars().first() is not None:
            raise ValueError(f"Location '{location_name}' already exists.")
        try:
            location = Location(name=location_name.strip())
            session.add(location)
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise ValueError(f"Location '{location}' already exists.")
        await session.refresh(location)
        return location.id

async def update_location(location: LocationModel):
    """
    Updates the name for an existing location with the given ID.
    :param location: The LocationModel instance containing the ID and new name.
    :raises ValueError: If the location ID does not exist or if the new location name is empty.
    """
    if location.name.strip() == "":
        raise ValueError("Location name cannot be empty.")

    async with AsyncSessionLocal() as session:
        # Fetch the location by ID
        result = await session.execute(
            select(Location).where(Location.id == location.id)
        )
        existing_location = result.scalars().first()

        if existing_location is None:
            raise ValueError(f"Location with ID '{location.id}' does not exist.")

        # Update the location name
        existing_location.name = location.name.strip()
        await session.commit()

async def delete_location(location_id: int):
    """
    Deletes the location with the given ID.
    :param location_id: The ID of the location to delete.
    :raises ValueError: If the location ID does not exist.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(delete(Location).where(Location.id == location_id))
        if result.rowcount == 0:
            raise ValueError(f"Location with ID '{location_id}' does not exist.")
        await session.commit()

async def list_locations() -> list[LocationModel]:
    """
    Lists all locations.
    :return: A list of LocationModel instances.
    """
    async with AsyncSessionLocal() as session:
        curr = (await session.scalars(select(Location))).all()
        return [LocationModel.model_validate(l) for l in curr]
