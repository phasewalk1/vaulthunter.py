from rich.console import Console


async def read_stream(stream, prefix, console=Console()):
    while True:
        line = await stream.readline()
        if line:
            console.print(f"[{prefix}] {line.decode().strip()}")
        else:
            break


async def read_stream_loading_bar(stream, prefix, console):
    buffer = b""
    while True:
        chunk = await stream.read(1024)
        if not chunk:
            break
        buffer += chunk
        try:
            decoded = buffer.decode()
            console.print(f"\n[{prefix}] {decoded}", end="")
            buffer = b""
        except UnicodeDecodeError:
            pass

    if buffer:
        try:
            decoded = buffer.decode()
            console.print(f"[{prefix}] {decoded}", end="")
        except UnicodeDecodeError:
            pass
