import os
from contextlib import asynccontextmanager

import aiosqlite

from database import migration_runner

DEFAULT_DB_PATH = "./data/ivy.db"

class DatabaseManager:
    """
    Manages the SQLite database connection and provides methods for executing queries and transactions.
    """

    def __init__(self):
        self.db_path = os.getenv("DB_PATH", DEFAULT_DB_PATH)
        self._db = None

    async def setup(self):
        """
        Sets up the database, establishes a connection and runs migrations
        """
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        await self.connect()

        await migration_runner.run_migrations(self._db)
        await self._db.commit()


    async def execute(self, sql: str, params: tuple = ()) -> aiosqlite.Cursor:
        """
        Executes a single SQL command with the provided parameters.
        :param sql: The SQL command to execute.
        :param params: A tuple of parameters to be used in the SQL command.
        :return: The cursor resulting from the execution of the SQL command.
        """
        cursor = await self._db.execute(sql, params)
        await self._db.commit()
        return cursor

    async def execute_transaction(self, sql_commands: list[tuple[str, tuple]]):
        """
        Executes a list of SQL commands as a single transaction. If any command fails, the entire transaction is rolled back.
        This is mainly used for executing commands that are related like item + tag + attachment linking.
        :param sql_commands: A list of tuples, where each tuple contains an SQL command and its corresponding parameters.
        """
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("BEGIN"):
                await db.execute("PRAGMA foreign_keys = ON;")
                for sql, params in sql_commands:
                    await db.execute(sql, params)
            await db.commit()

    async def fetch_all(self, sql: str, params: tuple = ()) -> list[tuple]:
        """
        Executes a SQL query and fetches all results.
        :param sql: The SQL query to execute.
        :param params: A tuple of parameters to be used in the SQL query.
        :return: A list of tuples representing the rows returned by the query.
        """
        cursor = await self._db.execute(sql, params)
        rows = await cursor.fetchall()
        return rows

    async def fetch_one(self, sql: str, params: tuple = ()):
        """
        Executes a SQL query and fetches a single result. Note that the whole query will still be executed even if
        only one result is returned. So this should only be used if you could add a LIMIT 1 which you should probably
        do for performance reasons then. Might add an automatic LIMIT later on.
        """
        # TODO: check if I cann add an automatic LIMIT 1 append to the query.
        cursor = await self._db.execute(sql, params)
        rows = await cursor.fetchone()
        return rows

    async def connect(self):
        self._db = await aiosqlite.connect(self.db_path)
        await self._db.execute("PRAGMA foreign_keys = ON;")

    @asynccontextmanager
    async def transaction(self):
        """
        Context manager for executing within a transaction.
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("BEGIN")
            await db.execute("PRAGMA foreign_keys = ON;")
            try:
                yield db
                await db.commit()
            except:
                await db.rollback()
                raise
