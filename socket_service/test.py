import asyncio
import os



async def read_output(stream):
    while True:
        line = await stream.readline()
        if not line:
            break
        print(line.decode().strip())  # Process or store the output as needed


async def run_command_and_monitor_output(command):
    try:
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Create two asyncio tasks to read standard output and standard error
        asyncio.create_task(read_output(process.stdout))
        asyncio.create_task(read_output(process.stderr))

        # Wait for the process to complete
        await process.wait()

    except asyncio.CancelledError:
        # The task was cancelled, terminate the process if it's still running
        if process.returncode is None:
            process.terminate()
            await process.wait()


if __name__ == "__main__":
    command = ["python", "workers/donkey.py"] + ["shrshn_aliev" + "__bot__.log", "shrshn_alyev"]

    asyncio.run(run_command_and_monitor_output(command))
