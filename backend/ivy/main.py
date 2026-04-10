import asyncio

from webserver import Webserver

async def main():
    webserver = Webserver()
    await webserver.run_server()

if __name__ == '__main__':
    asyncio.run(main())