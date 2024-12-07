import aiohttp
import asyncio
from aiohttp import web
import os


class Coordinator:
    """Manages workers and aggregates results."""

    def __init__(self, port: int):
        self.port = port
        self.workers = {}
        self.results = {}

    async def register_worker(self, request):
        """Register a new worker."""
        data = await request.json()
        worker_id = data["worker_id"]
        self.workers[worker_id] = {"healthy": True}
        print(f"Worker {worker_id} registered.")
        return web.Response(text="Worker registered.")

    async def distribute_work(self, filepath: str):
        """Distribute log file chunks among workers."""
        file_size = os.path.getsize(filepath)
        chunk_size = 1024 * 1024  # 1 MB
        workers = list(self.workers.keys())
        num_workers = len(workers)

        if num_workers == 0:
            print("No workers available.")
            return

        tasks = []
        for i, worker_id in enumerate(workers):
            start = i * chunk_size
            size = min(chunk_size, file_size - start)
            task = asyncio.create_task(self.assign_work(worker_id, filepath, start, size))
            tasks.append(task)

        await asyncio.gather(*tasks)

    async def assign_work(self, worker_id: str, filepath: str, start: int, size: int):
        """Assign a chunk of work to a worker."""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {"filepath": filepath, "start": start, "size": size}
                worker_url = f"http://localhost:{worker_id}/process"
                await session.post(worker_url, json=payload)
        except Exception as e:
            print(f"Worker {worker_id} failed: {e}")
            await self.handle_worker_failure(worker_id)

    async def handle_worker_failure(self, worker_id: str):
        """Handle worker failure and reassign its tasks."""
        print(f"Reassigning tasks of failed worker {worker_id}.")
        self.workers.pop(worker_id, None)

    def start(self):
        """Start the coordinator server."""
        app = web.Application()
        app.router.add_post("/register", self.register_worker)
        web.run_app(app, port=self.port)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Coordinator Node")
    parser.add_argument("--port", type=int, required=True, help="Port for the coordinator")
    args = parser.parse_args()

    coordinator = Coordinator(port=args.port)
    coordinator.start()
