# **Log Analyzer System**

## **Business Objective**
The **Log Analyzer System** is designed to process and analyze log files efficiently in distributed environments. It uses a coordinator-worker architecture to ensure fast, reliable log analysis with the ability to handle worker failures. The system monitors key performance metrics such as processing speed, memory usage, and result accuracy while maintaining resource efficiency and scalability.

---

## **Key Features**
1. **Distributed Processing**: Tasks are distributed across multiple worker nodes to ensure parallel processing.
2. **Worker Failure Recovery**: Simulates and recovers from worker failures, ensuring uninterrupted processing.
3. **Performance Monitoring**: Measures metrics like processing speed, memory usage, and recovery time.
4. **Result Accuracy**: Compares output against predefined metrics to validate accuracy.

---

## **Setup Instructions**

### **Pre-requisites**
- Python 3.9 or higher
- Virtual environment setup

### **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/chainscore-hiring/log-analyzer-assessment
   cd log-analyzer-assessment
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/MacOS
   venv\Scripts\activate  # For Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### **Starting the System**
1. **Run the coordinator**:
   ```bash
   python coordinator.py --port 8000
   ```
2. **Run workers in separate terminals**:
   ```bash
   python worker.py --id alice --port 8001 --coordinator http://localhost:8000
   python worker.py --id bob --port 8002 --coordinator http://localhost:8000
   python worker.py --id charlie --port 8003 --coordinator http://localhost:8000
   ```

### **Testing the System**
1. Use the provided sample logs in `test_vectors/logs/`.
2. Run test scenarios:
   ```bash
   pytest --asyncio-mode=auto
   ```

---

## **System Design**

### **Coordinator**
- **Responsibilities**:
  - Manage worker nodes.
  - Distribute tasks across workers.
  - Aggregate results and handle errors.
- **Key Methods**:
  - `distribute_work`: Splits logs into chunks and assigns to workers.
  - `monitor_workers`: Monitors worker health and reallocates tasks if needed.

### **Worker**
- **Responsibilities**:
  - Process assigned log chunks.
  - Report health status to the coordinator.
  - Handle chunk-level errors.
- **Key Methods**:
  - `process_chunk`: Processes a chunk of the log file and calculates metrics.
  - `report_health`: Reports status and resource usage to the coordinator.

### **Analysis Engine**
- **Responsibilities**:
  - Calculate key performance metrics like response time, error rate, and throughput.
  - Compare results with predefined benchmarks.
- **Key Methods**:
  - `analyze_logs`: Parses logs and computes metrics.
  - `validate_results`: Compares results with `expected.py`.

---

## **Performance Results**
1. **Processing Speed**:
   - Processes at least **100MB/s**.
   - Tested with a 1GB log file (`large.log`) in `test_vectors/logs/`.
2. **Memory Usage**:
   - Maintains memory usage under **500MB** during processing.
3. **Failure Recovery Time**:
   - Automatically reassigns tasks to healthy workers in case of failure.
4. **Result Accuracy**:
   - Matches expected metrics with a **tolerance of 1%** (using `pytest.approx`).

---

## **Testing**
- **Test Scenarios**:
  1. **Normal Log Processing**:
     - Verifies processing with all workers active.
  2. **Worker Failure**:
     - Tests task reassignment when a worker fails mid-process.
  3. **Malformed Logs**:
     - Ensures system handles invalid log lines without crashing.
  4. **High Latency**:
     - Tests worker performance under high-latency conditions.

- **Commands**:
   ```bash
   pytest --asyncio-mode=auto
   ```

---

## **Design Decisions**
1. **Coordinator-Worker Architecture**:
   - Ensures scalability and distributed processing.
2. **Chunk-Based Log Processing**:
   - Processes logs in manageable chunks to reduce memory overhead.
3. **Error Tolerance**:
   - Implements robust error handling to manage malformed logs and worker failures.
4. **Health Monitoring**:
   - Periodically checks worker health for optimal performance.

---

## **Future Enhancements**
- Implement load balancing for resource optimization.
- Introduce real-time processing capabilities for streaming logs.
- Extend testing to cover edge cases like network partitioning.

---

## **Folder Structure**
```
log-analyzer-assessment/
├── coordinator.py        # Coordinator implementation
├── worker.py             # Worker implementation
├── analysis_engine.py    # Analysis engine for metrics calculation
├── test_vectors/         # Sample logs and expected results
│   ├── logs/
│   ├── expected.py
│   ├── network.py
│   └── performance.py
├── tests/                # Test cases
│   └── test_cases.py
├── README.md             # Documentation
├── requirements.txt      # Dependencies
└── venv/                 # Virtual environment
```
