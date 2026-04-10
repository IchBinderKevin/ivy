"""initial migration

Revision ID: 001
Revises: 
Create Date: 2026-04-09 19:24:02.968511

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # old mig 001
    op.execute("""
        CREATE TABLE IF NOT EXISTS locations (id INTEGER PRIMARY KEY, name TEXT NOT NULL, 
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, parent_location_id INTEGER, FOREIGN KEY (parent_location_id) 
        REFERENCES locations(id) ON DELETE SET NULL);
    """)
    op.execute(
        "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT NOT NULL, description TEXT, image TEXT, "
        "location_id INTEGER, quantity INTEGER, date_of_purchase TEXT, buy_price REAL, bought_from TEXT, "
        "serial_number TEXT, model_number TEXT, isbn TEXT, notes TEXT, "
        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(location_id) REFERENCES locations(id));")

    op.execute("CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY, name TEXT NOT NULL, "
               "color TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")

    op.execute("CREATE TABLE IF NOT EXISTS item_tag_mappings (item_id INTEGER, tag_id INTEGER, "
               "FOREIGN KEY(item_id) REFERENCES items(id), FOREIGN KEY(tag_id) REFERENCES tags(id), "
               "PRIMARY KEY(item_id, tag_id));")

    op.execute("CREATE TABLE IF NOT EXISTS item_attachment_mappings (id INTEGER PRIMARY KEY, item_id INTEGER, "
               "attachment_path TEXT, FOREIGN KEY(item_id) REFERENCES items(id));")

    # old mig 002
    op.execute("ALTER TABLE item_tag_mappings RENAME TO item_tag_mappings_old;")
    op.execute("""
        CREATE TABLE item_tag_mappings (
            item_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE,
            FOREIGN KEY(tag_id) REFERENCES tags(id) ON DELETE CASCADE,
            PRIMARY KEY(item_id, tag_id)
        );
    """)
    op.execute("INSERT INTO item_tag_mappings SELECT * FROM item_tag_mappings_old;")

    op.execute("ALTER TABLE item_attachment_mappings RENAME TO item_attachment_mappings_old;")
    op.execute("""
        CREATE TABLE item_attachment_mappings (
            id INTEGER PRIMARY KEY,
            item_id INTEGER,
            attachment_path TEXT,
            FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE
        );
    """)
    op.execute("INSERT INTO item_attachment_mappings SELECT * FROM item_attachment_mappings_old;")

    op.execute("DROP TABLE item_tag_mappings_old;")
    op.execute("DROP TABLE item_attachment_mappings_old;")


def downgrade() -> None:
    """Downgrade schema."""
    pass
