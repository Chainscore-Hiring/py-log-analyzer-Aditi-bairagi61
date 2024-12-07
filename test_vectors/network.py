### Network Scenarios
class NetworkScenarios:
    @staticmethod
    async def normal():
        """Simulates all workers being responsive."""
        return {
            "worker1": {"healthy": True, "latency": 10},  # Latency in ms
            "worker2": {"healthy": True, "latency": 15},
            "worker3": {"healthy": True, "latency": 12}
        }

    @staticmethod
    async def worker_failure():
        """Simulates a failure in worker 2 after 50% processing."""
        return {
            "worker1": {"healthy": True, "latency": 10},
            "worker2": {"healthy": False, "fail_at": 0.5},  # Fails midway
            "worker3": {"healthy": True, "latency": 12}
        }

    @staticmethod
    async def high_latency():
        """Simulates worker 3 experiencing high latency."""
        return {
            "worker1": {"healthy": True, "latency": 10},
            "worker2": {"healthy": True, "latency": 15},
            "worker3": {"healthy": True, "latency": 1000}  # High latency
        }
