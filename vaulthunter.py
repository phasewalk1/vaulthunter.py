import asyncio
import os
import signal
import click
from rich.console import Console

# Assuming console_streams.py is imported as before
from console_streams import read_stream, read_stream_loading_bar

console = Console()
processes = []


async def run_command(command, cwd, prefix):
    process = await asyncio.create_subprocess_shell(
        command,
        cwd=cwd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        preexec_fn=os.setsid,  # This is still crucial
    )
    processes.append(process)  # Add the new process to the list
    asyncio.create_task(read_stream(process.stdout, prefix))
    asyncio.create_task(read_stream_loading_bar(process.stderr, prefix, console))
    return process


async def terminate_processes():
    for process in processes:
        if process:
            os.killpg(
                os.getpgid(process.pid), signal.SIGTERM
            )  # Attempt to terminate gracefully
            try:
                await asyncio.wait_for(process.wait(), timeout=5)
            except asyncio.TimeoutError:
                os.killpg(
                    os.getpgid(process.pid), signal.SIGKILL
                )  # Force kill if necessary
            console.print(f"Process {process.pid} terminated", style="bold red")
    console.print("All processes have been terminated.", style="bold green")


def signal_handler():
    asyncio.create_task(terminate_processes())


async def start_backend():
    return await run_command(
        "pipenv run uvicorn app:app --host 0.0.0.0 --reload", "./fastapi", "Backend"
    )


async def start_frontend():
    return await run_command("npm start", "./electron", "Frontend")


@click.command()
@click.option(
    "--vault", type=click.Path(exists=True), help="Path to an Obsidian vault."
)
def cli(vault):
    asyncio.run(main(vault))


async def main(vault):
    os.environ["VAULT"] = vault
    console.print("Starting VaultHunter...", style="bold blue")

    # Setup signal handlers
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)

    backend_process = await start_backend()
    frontend_process = await start_frontend()

    # Wait for processes indefinitely
    await asyncio.gather(*[p.wait() for p in processes])


if __name__ == "__main__":
    cli()
