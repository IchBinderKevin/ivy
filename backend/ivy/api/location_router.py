from fastapi import APIRouter, status, HTTPException, Response

from models.location_model import LocationModel
from services import location_service


def create_locations_router() -> APIRouter:
    """
    Creates the router for location related endpoints.
    """
    router = APIRouter()
    @router.post("/create")
    @router.put("/create")
    async def create_location(location: LocationModel):
        """
        Creates a new location.
        :param location: The LocationModel model passed from the frontend.
        """
        try:
            await location_service.create_location(location.name)
            return Response(status_code=status.HTTP_201_CREATED)
        except ValueError as e:
            raise HTTPException(400, str(e))

    @router.get("/list")
    async def list_locations() -> list[LocationModel]:
        """
        Lists all locations.
        :return: A list of LocationModel instances.
        """
        locations = await location_service.list_locations()
        return locations

    # delete location
    @router.delete("/delete/{location_id}")
    async def delete_location(location_id: int):
        """
        Deletes a location by its ID.
        :param location_id: The ID of the location to delete.
        """
        try:
            await location_service.delete_location(location_id)
            return Response(status_code=status.HTTP_200_OK)
        except ValueError as e:
            raise HTTPException(400, str(e))

    # edit location
    @router.post("/edit")
    async def edit_location(location: LocationModel):
        """
        Edits a location's name by its ID.
        :param location: The LocationModel model passed from the frontend containing the ID and new name.
        """
        try:
            await location_service.update_location(location)
            return Response(status_code=status.HTTP_200_OK)
        except ValueError as e:
            raise HTTPException(400, str(e))

    return router
