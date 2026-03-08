import asyncio
from asyncio import Future

from webserver import Webserver
from database.database_manager import DatabaseManager

async def main():
    db = DatabaseManager()
    await db.setup()
    webserver = Webserver(db)
    await webserver.run_server()
    await Future()

if __name__ == '__main__':
    asyncio.run(main())