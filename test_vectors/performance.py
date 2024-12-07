import time
from test_vectors.network import NetworkScenarios
from coordinator import Coordinator
from worker import Worker
from test_vectors.test_data import generate_test_logs

### Performance Tests
async def test_processing_speed():
    """Ensures processing meets speed requirements."""
    coordinator = Coordinator(port=8000)
    workers = [
        Worker("worker1", "localhost:8000"),
        Worker("worker2", "localhost:8000"),
        Worker("worker3", "localhost:8000")
    ]
    
    # Generate test data
    generate_test_logs(size_mb=1024, path="test_vectors/logs/large.log")
    
    # Measure processing time
    start_time = time.time()
    await coordinator.process_file("test_vectors/logs/large.log")
    duration = time.time() - start_time
    
    # Assert processing speed >= 100MB/s
    assert (1024 / duration) >= 100, f"Processing speed below 100MB/s: {1024 / duration} MB/s"

async def test_memory_usage():
    """Ensures memory usage remains within limits."""
    import psutil
    worker = Worker("worker1", "localhost:8000")
    process = psutil.Process()
    
    initial_memory = process.memory_info().rss
    await worker.process_chunk("test_vectors/logs/large.log", 0, 1024 * 1024 * 100)  # 100MB
    peak_memory = process.memory_info().rss
    
    # Assert memory usage < 500MB
    assert (peak_memory - initial_memory) < 500 * 1024 * 1024, "Memory usage exceeded 500MB"
