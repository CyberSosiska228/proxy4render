import asyncio
from asyncio import StreamReader, StreamWriter

async def handle_client(reader, writer):
    writer.write(b"Meow\r\n")
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 1080)
    await server.serve_forever()

asyncio.run(main())
