from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DEFAULT_DB_PATH = "./data/ivy.db"
DATABASE_URL = f"sqlite+aiosqlite:///{DEFAULT_DB_PATH}"

engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)

@event.listens_for(engine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Event listener to set SQLite PRAGMA settings on each new connection to allow for CASCADE deletes.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
