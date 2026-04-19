import asyncio
import os

async def handle_client(reader, writer):
    writer.write(b"Meow\r\n")
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main():
    port = int(os.environ.get("PORT", 8080))
    server = await asyncio.start_server(handle_client, '0.0.0.0', port)
    print(f"Server is listening on port {port}")
    await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
