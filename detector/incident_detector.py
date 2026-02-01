import json
import os

class IncidentDetector:
    def __init__(self):
        # Thresholds defined for the Decision Tree 
        self.MEMORY_THRESHOLD = 90  # Percent
        self.DISK_THRESHOLD = 95    # Percent
        self.LATENCY_THRESHOLD = 500 # Milliseconds (0.5s)
        self.ERROR_RATE_THRESHOLD = 0.15 # 15% error rate

    def load_telemetry(self, file_path):
        """Reads simulated JSON telemetry data[cite: 6]."""
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: {file_path} not found.")
            return None

    def parse_logs(self, log_content):
        """
        Parses raw log text to detect incidents based on string patterns.
        Returns the incident details including all matching log lines as evidence.
        """
        log_lower = log_content.lower()
        lines = log_content.splitlines()
        
        # Helper to find ALL lines matching a list of patterns
        def find_evidence(patterns):
            matches = [line.strip() for line in lines if any(p in line.lower() for p in patterns)]
            if matches:
                return "\n".join(matches)
            return "Log pattern detected."

        # --- PATTERN 1: Disk Full ---
        disk_patterns = ["no space left on device", "disk space critically low", "100% full"]
        if any(p in log_lower for p in disk_patterns):
            return {
                "incident": "Disk Full",
                "action": "Auto-remediate",
                "reason": "Log analysis detected critical disk space warnings.",
                "evidence": find_evidence(disk_patterns),
                "suggested_fix": "Clear temporary log files and expand volume."
            }

        # --- PATTERN 2: API Timeout ---
        timeout_patterns = ["timeout", "timed out", "slow api response", "high latency"]
        if any(p in log_lower for p in timeout_patterns):
            return {
                "incident": "API Timeout",
                "action": "Escalate",
                "reason": "Log analysis detected extensive timeout errors.",
                "evidence": find_evidence(timeout_patterns),
                "suggested_fix": "Check downstream microservices and network health."
            }

        # --- PATTERN 3: Memory Leak ---
        memory_patterns = ["malloc", "allocate resources", "outofmemory", "heap space", "segmentation fault", "corrupted top size"]
        if any(p in log_lower for p in memory_patterns):
            return {
                "incident": "Memory Leak",
                "action": "Human-in-loop approval",
                "reason": "Log analysis found memory allocation failures.",
                "evidence": find_evidence(memory_patterns),
                "suggested_fix": "Restart service and check for unclosed database connections."
            }
            
        return {
            "incident": "None", 
            "action": "Monitor", 
            "reason": "No critical error patterns found in logs.",
            "evidence": "N/A"
        }

    def analyze(self, telemetry_data):
        """
        Implementation of the Decision Tree with Time-Series Trends:
        Auto-fix -> Human-in-loop -> Escalate
        
        Now supports both structured JSON (list) and raw logs (str).
        """
        
        # Branch 1: Log Analysis (String)
        if isinstance(telemetry_data, str):
            return self.parse_logs(telemetry_data)

        # Branch 2: Metrics Analysis (JSON List)
        if not telemetry_data or not isinstance(telemetry_data, list):
            return None

        # Sort by timestamp just in case
        data = sorted(telemetry_data, key=lambda x: x.get('timestamp', ''))
        latest = data[-1]
        
        # Calculate moving averages (last 3 points)
        window = data[-3:] if len(data) >= 3 else data
        avg_memory = sum(d.get('memory_usage', 0) for d in window) / len(window)
        avg_disk = sum(d.get('disk_usage', 0) for d in window) / len(window)
        avg_latency = sum(d.get('latency', 0) for d in window) / len(window)
        avg_error = sum(d.get('error_rate', 0) for d in window) / len(window)

        # --- INCIDENT 1: Disk Full (Auto-remediate) ---
        # Logic: Consistent high disk usage
        if avg_disk > self.DISK_THRESHOLD:
            return {
                "incident": "Disk Full",
                "action": "Auto-remediate",
                "reason": f"Sustained disk usage at {avg_disk:.1f}% exceeds threshold of {self.DISK_THRESHOLD}%.",
                "suggested_fix": "Clear temporary log files and expand volume."
            }

        # --- INCIDENT 2: Memory Leak (Human-in-loop) ---
        # Logic: Trend analysis - Is memory strictly increasing?
        mem_values = [d.get('memory_usage', 0) for d in window]
        is_increasing = all(x < y for x, y in zip(mem_values, mem_values[1:]))
        
        if avg_memory > self.MEMORY_THRESHOLD and is_increasing:
            return {
                "incident": "Memory Leak",
                "action": "Human-in-loop approval",
                "reason": f"Memory usage shows consistent upward trend: {mem_values}%.",
                "suggested_fix": "Restart service and check for unclosed database connections."
            }

        # --- INCIDENT 3: API Timeout (Escalate) ---
        # Logic: High latency or error rate spikes
        if avg_latency > self.LATENCY_THRESHOLD or avg_error > self.ERROR_RATE_THRESHOLD:
            return {
                "incident": "API Timeout",
                "action": "Escalate",
                "reason": f"High latency ({avg_latency:.1f}ms) or Error Rate ({avg_error:.2f}) detected.",
                "suggested_fix": "Check downstream microservices and network health."
            }

        # --- SUCCESS METRIC: Handle False Positives  ---
        # Logic: Transient spike check (latest high, average low)
        if latest.get('cpu_usage', 0) > 90 and (sum(d.get('cpu_usage', 0) for d in data) / len(data)) < 50:
             return {
                "incident": "False Positive",
                "action": "Ignore",
                "reason": "Transient CPU spike detected and recovered. No impact on service health."
            }

        return {"incident": "None", "action": "Monitor", "reason": "All metrics within normal bounds."}

# Testing the Logic
if __name__ == "__main__":
    detector = IncidentDetector()
    
    # You can test by pointing to your JSON files
    print("Testing Detection System...")

# Functional Wrapper for easier integration
# Functional Wrapper for easier integration
def detect_incident(telemetry_data):
    """
    Wrapper around IncidentDetector to return normalized incident labels
    for the decision engine.
    """

    # ✅ Import here to avoid circular / load-time issues
    from detector.incident_detector import IncidentDetector

    detector = IncidentDetector()
    result = detector.analyze(telemetry_data)

    if not result:
        return "NO_INCIDENT"

    incident_raw = result.get("incident", "None")

    mapping = {
        "Disk Full": "DISK_FULL",
        "Memory Leak": "MEMORY_LEAK",
        "API Timeout": "API_TIMEOUT",
        "False Positive": "NO_INCIDENT",
        "None": "NO_INCIDENT"
    }

    return mapping.get(incident_raw, "NO_INCIDENT")
