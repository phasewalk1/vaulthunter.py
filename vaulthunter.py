import asyncio
import os
import signal

import click
from rich.console import Console

console = Console()


async def read_stream(stream, prefix):
    while True:
        line = await stream.readline()
        if line:
            console.print(f"[{prefix}] {line.decode().strip()}")
        else:
            break


async def read_stream_loading_bar(stream, prefix, console):
    buffer = b""  # Use a bytes buffer
    while True:
        chunk = await stream.read(1024)  # Read in chunks of 1KB
        if not chunk:
            break  # End of stream
        buffer += chunk
        try:
            # Attempt to decode the buffer to string and print
            decoded = buffer.decode()
            console.print(f"\n[{prefix}] {decoded}", end="")
            buffer = b""  # Reset buffer after successful decode
        except UnicodeDecodeError:
            # If decode fails, handle or ignore undecodable bytes
            # Here we choose to ignore and reset the buffer, but you could also log hex representation etc.
            pass

    # Handle any remaining bytes in the buffer
    if buffer:
        try:
            decoded = buffer.decode()
            console.print(f"[{prefix}] {decoded}", end="")
        except UnicodeDecodeError:
            pass  # Ignore or handle remaining undecodable bytes as needed


async def start_process(command, cwd, prefix):
    # Note: Using asyncio.create_subprocess_shell for an async subprocess
    process = await asyncio.create_subprocess_shell(
        " ".join(command),
        cwd=cwd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        preexec_fn=os.setsid,
    )

    # Create tasks for reading stdout and stderr simultaneously
    await asyncio.gather(
        read_stream(process.stdout, prefix),
        read_stream_loading_bar(process.stderr, prefix, console),
    )
    return process


async def start_backend():
    return await start_process(
        ["pipenv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--reload"],
        "./fastapi",
        "Backend",
    )


async def start_frontend():
    return await start_process(["npm", "start"], "./electron", "Frontend")


def stop_processes(processes):
    for process in processes:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    console.print("All processes stopped.", style="bold red")


@click.group()
def cli():
    pass


@click.option(
    "--vault", type=click.Path(exists=True), help="Path to an Obsidian vault."
)
@click.command()
def start(vault):
    """Starts the Electron frontend and FastAPI backend."""
    console.print("Starting the VaultHunter application...", style="bold blue")
    console.print(f"Using vault at {vault}", style="bold purple")

    os.environ["VAULT"] = vault

    loop = asyncio.get_event_loop()
    backend, frontend = loop.run_until_complete(
        asyncio.gather(start_backend(), start_frontend())
    )

    console.print("VaultHunter is running. Press Ctrl+C to stop.", style="bold green")

    # Stop processes on KeyboardInterrupt
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        stop_processes([backend, frontend])


cli.add_command(start)

if __name__ == "__main__":
    cli()
