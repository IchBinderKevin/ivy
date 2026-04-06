from email.mime import image

from aiosqlite import Connection

from database.database_manager import DatabaseManager
from models.item_model import ItemModel
from utils.validation_util import validate_safe


class ItemRepository:
    """
    Repository for managing items in the database, providing methods for CRUD
    operations and handling item attachments and tags.
    """

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    async def create(self, db: Connection, item_model: ItemModel):
        """
        Creates a new item in the database using the provided ItemModel instance.
        :param db: The database connection to use for the operation.
        :param item_model: The ItemModel instance containing the item details to be created.
        :return: The ID of the newly created item.
        """
        item = await db.execute("INSERT INTO items (name, description, image, location_id, "
                                "quantity, date_of_purchase, buy_price, bought_from, "
                                "serial_number, model_number, isbn, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                                (item_model.name, item_model.description, item_model.image, item_model.location.id if item_model.location is not None else None,
                                 item_model.quantity,
                                 item_model.date_of_purchase, item_model.buy_price, item_model.bought_from,
                                 item_model.serial_number, item_model.model_number, item_model.isbn, item_model.notes))
        return item.lastrowid

    async def update_image_path(self, db: Connection, item_id: int, image_path: str):
        """
        Updates the image path for the specified item in the database.
        Necessary because the image path is not finalized until after the item is
        created and we have the item ID to associate it with.
        :param db: The database connection to use for the operation.
        :param item_id: The ID of the item for which to update the image path.
        :param image_path: The new image path to be set for the specified item.
        """
        await db.execute("UPDATE items SET image = ? WHERE id = ?;", (image_path, item_id))

    async def add_attachments(self, db: Connection, item_model: ItemModel):
        """
        Adds attachments for the specified item in the database.
        :param db: The database connection to use for the operation.
        :param item_model: The ItemModel instance containing the item ID and attachments to be added
        """
        for attachment in item_model.attachments:
            await db.execute("INSERT INTO item_attachment_mappings (item_id, attachment_path) VALUES (?, ?);",
                             (item_model.id, attachment.path))

    async def get_attachments(self, item_id: int) -> list[str]:
        """
        Retrieves the attachment paths for the specified item ID from the database.
        :param item_id: The ID of the item for which to retrieve attachments.
        :return: A list of attachment paths associated with the specified item ID.
        """
        rows = await self.db_manager.fetch_all(
            "SELECT attachment_path FROM item_attachment_mappings WHERE item_id = ?;",
            (item_id,)
        )
        attachment_paths = [row[0] for row in rows]
        return attachment_paths

    async def assign_tags(self, db: Connection, item_model: ItemModel):
        """
        Assigns tags to the specified item in the database.
        :param db: The database connection to use for the operation.
        :param item_model: The ItemModel instance containing the item ID and tag IDs to be assigned.
        """
        for tag in item_model.tags:
            await db.execute("INSERT INTO item_tag_mappings (item_id, tag_id) VALUES (?, ?);",
                             (item_model.id, tag.id))

    async def get_assigned_tag_ids(self, item_id: int) -> list[int]:
        """
        Retrieves the tag IDs assigned to the specified item ID from the database.
        :param item_id: The ID of the item for which to retrieve assigned tag IDs.
        :return: A list of tag IDs assigned to the specified item ID.
        """
        rows = await self.db_manager.fetch_all(
            "SELECT tag_id FROM item_tag_mappings WHERE item_id = ?;",
            (item_id,)
        )
        tag_ids = [row[0] for row in rows]
        return tag_ids

    async def list_all(self) -> list[ItemModel]:
        """
        Lists all items in the database and maps them to ItemModel instances.
        :return: A list of ItemModel instances representing all items in the database.
        """
        columns = ["id", "name", "description", "image", "location_id",
                                "quantity", "date_of_purchase", "buy_price", "bought_from",
                                "serial_number", "model_number", "isbn", "notes"]
        items = await self.db_manager.fetch_all(
            f"SELECT {",".join(columns)} FROM items;")
        mapped_items = []

        for item in items:
            mapped_items.append(dict(zip(columns, item)))
        item_models = [validate_safe(item, ItemModel) for item in mapped_items]
        return item_models

    async def does_item_id_exist(self, item_id: int) -> bool:
        """
        Checks if an item with the specified ID exists in the database.
        :param item_id: The ID of the item to check for existence.
        :return: True if an item with the specified ID exists, False otherwise.
        """
        row = await self.db_manager.fetch_one(
            "SELECT id FROM items WHERE id = ?;",
            (item_id,)
        )
        return row is not None

    async def delete(self, item_id: int):
        await self.db_manager.execute(
            "DELETE FROM items WHERE id = ?;",
            (item_id,)
        )