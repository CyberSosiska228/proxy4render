import asyncio
import os
import sys

async def handle_client(reader, writer):
    writer.write(b"Meow\r\n")
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main():
    port = int(os.environ.get("PORT", 8080))
    server = await asyncio.start_server(handle_client, '0.0.0.0', port)
    sys.stderr.write(f"Server listening on port {port}\n")
    sys.stderr.flush()
    await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
