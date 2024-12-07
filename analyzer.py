from typing import Dict


class Analyzer:
    """Calculates real-time metrics from results."""

    def __init__(self):
        self.metrics = {"error_rate": 0, "avg_response_time": 0, "requests_per_second": 0}
        self.error_count = 0
        self.request_count = 0

    def update_metrics(self, new_data: Dict):
        """Update metrics with new data from workers."""
        self.error_count += new_data.get("error_count", 0)
        self.request_count += new_data.get("request_count", 0)
        if self.request_count > 0:
            self.metrics["avg_response_time"] = (
                self.metrics.get("avg_response_time", 0) + new_data.get("avg_response_time", 0)
            ) / self.request_count
        self.metrics["error_rate"] = self.error_count / max(1, self.request_count)

    def get_current_metrics(self) -> Dict:
        """Return current calculated metrics."""
        return self.metrics
