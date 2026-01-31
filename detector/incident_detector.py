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

    def analyze(self, telemetry_data):
        """
        Implementation of the Decision Tree: 
        Auto-fix -> Human-in-loop -> Escalate 
        """
        if not telemetry_data:
            return None

        latest = telemetry_data[-1]
        # Compare with previous state to detect trends (e.g., for Memory Leaks)
        previous = telemetry_data[-2] if len(telemetry_data) > 1 else latest

        # --- INCIDENT 1: Disk Full (Auto-remediate) ---
        if latest['disk_usage'] > self.DISK_THRESHOLD:
            return {
                "incident": "Disk Full",
                "action": "Auto-remediate",
                "reason": f"Disk usage at {latest['disk_usage']}% exceeds safety threshold of {self.DISK_THRESHOLD}%.",
                "suggested_fix": "Clear temporary log files and expand volume."
            }

        # --- INCIDENT 2: Memory Leak (Human-in-loop) ---
        # Logic: High memory AND it is steadily increasing 
        if latest['memory_usage'] > self.MEMORY_THRESHOLD and latest['memory_usage'] > previous['memory_usage']:
            return {
                "incident": "Memory Leak",
                "action": "Human-in-loop approval",
                "reason": f"Memory rose from {previous['memory_usage']}% to {latest['memory_usage']}% without traffic spike.",
                "suggested_fix": "Restart service and check for unclosed database connections."
            }

        # --- INCIDENT 3: API Timeout (Escalate) ---
        # Logic: High latency or high error rates 
        if latest.get('latency', 0) > self.LATENCY_THRESHOLD or latest.get('error_rate', 0) > self.ERROR_RATE_THRESHOLD:
            return {
                "incident": "API Timeout",
                "action": "Escalate",
                "reason": f"Latency ({latest.get('latency')}ms) or Error Rate ({latest.get('error_rate')}) is too high.",
                "suggested_fix": "Check downstream microservices and network health."
            }

        # --- SUCCESS METRIC: Handle False Positives  ---
        # If there's a tiny spike that immediately dropped, we ignore it.
        if latest['cpu_usage'] > 90 and previous['cpu_usage'] < 30:
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
    # Example: test_data = detector.load_telemetry('telemetry/memory_leak.json')
    # print(detector.analyze(test_data))