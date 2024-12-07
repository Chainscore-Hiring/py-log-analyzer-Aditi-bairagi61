import aiohttp
import asyncio
import aiofiles
from datetime import datetime
from typing import Dict


class Worker:
    """Processes log chunks and reports results."""

    def __init__(self, worker_id: str, coordinator_url: str):
        self.worker_id = worker_id
        self.coordinator_url = coordinator_url

    async def process_chunk(self, filepath: str, start: int, size: int) -> Dict:
        """Process a chunk of the log file and return metrics."""
        metrics = {"error_count": 0, "request_count": 0, "avg_response_time": 0}
        total_response_time = 0

        async with aiofiles.open(filepath, mode="r") as f:
            await f.seek(start)
            chunk = await f.read(size)

            for line in chunk.splitlines():
                parts = line.split()
                if len(parts) < 4:
                    continue
                timestamp, level, *message = parts
                if level == "ERROR":
                    metrics["error_count"] += 1
                elif "Request processed in" in line:
                    metrics["request_count"] += 1
                    response_time = int(message[-1].replace("ms", ""))
                    total_response_time += response_time

        if metrics["request_count"] > 0:
            metrics["avg_response_time"] = total_response_time / metrics["request_count"]
        return metrics

    async def report_health(self) -> None:
        """Send heartbeat to the coordinator."""
        async with aiohttp.ClientSession() as session:
            try:
                payload = {"worker_id": self.worker_id}
                await session.post(f"{self.coordinator_url}/health", json=payload)
            except Exception as e:
                print(f"Failed to report health: {e}")

    async def register(self):
        """Register worker with the coordinator."""
        async with aiohttp.ClientSession() as session:
            payload = {"worker_id": self.worker_id}
            await session.post(f"{self.coordinator_url}/register", json=payload)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Worker Node")
    parser.add_argument("--worker_id", required=True, help="Unique ID for the worker")
    parser.add_argument("--coordinator_url", required=True, help="URL of the coordinator")
    args = parser.parse_args()

    worker = Worker(worker_id=args.worker_id, coordinator_url=args.coordinator_url)
    asyncio.run(worker.register())
