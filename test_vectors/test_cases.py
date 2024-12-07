import pytest
from coordinator import Coordinator
from worker import Worker
from test_vectors.network import NetworkScenarios

### Test Cases
async def test_normal_processing():
    """Tests normal log processing with all workers active."""
    coordinator = Coordinator(port=8000)
    workers = [
        Worker("worker1", "localhost:8000"),
        Worker("worker2", "localhost:8000"),
        Worker("worker3", "localhost:8000")
    ]
    
    # Start workers and coordinator
    await coordinator.start()
    for worker in workers:
        await worker.start()
    
    # Process logs and verify results
    results = await coordinator.process_file("test_vectors/logs/normal.log")
    assert results["avg_response_time"] == pytest.approx(109.0, rel=1e-2)
    assert results["error_rate"] == 0.0
    assert results["requests_per_second"] == pytest.approx(50.0, rel=1e-2)

async def test_worker_failure():
    """Tests system resilience to worker failure."""
    coordinator = Coordinator(port=8000)
    workers = [
        Worker("worker1", "localhost:8000"),
        Worker("worker2", "localhost:8000"),
        Worker("worker3", "localhost:8000")
    ]
    
    # Simulate worker failure and verify completion
    await NetworkScenarios.worker_failure()
    results = await coordinator.process_file("test_vectors/logs/normal.log")
    assert results["total_requests"] == 3000

async def test_malformed_logs():
    """Tests handling of malformed logs."""
    coordinator = Coordinator(port=8000)
    workers = [Worker("worker1", "localhost:8000")]
    
    # Process malformed logs and verify
    results = await coordinator.process_file("test_vectors/logs/malformed.log")
    assert results["malformed_lines"] == 30
    assert results["total_requests"] == 200
