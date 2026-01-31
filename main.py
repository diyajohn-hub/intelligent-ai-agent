from detector.incident_detector import IncidentDetector
from agent import IncidentResponseAgent
import os
import json

from llm.root_cause_agent import explain_root_cause
from decision.decision_engine import make_decision
from utils.metrics import calculate_mttd, is_false_alert, estimate_resolution_time
from actions.remediation import apply_fix
from agent import IncidentResponseAgent
import os
import json
import sys

# Ensure UTF-8 output for emojis on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def load_telemetry(filepath):
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return None
    with open(filepath, 'r') as file:
        return json.load(file)

def print_report(report):
    if isinstance(report, str):
        print(report)
        return

    print("=" * 70)
    print("INCIDENT RESPONSE REPORT")
    print("=" * 70)
    print(f"INCIDENT TYPE: {report['incident_type']}\nSEVERITY: {report['decision']['severity']}\n")
    print("-" * 70 + "\nANALYSIS\n" + "-" * 70)
    print(f"Confidence Score: {report['confidence']:.2f}\nRoot Cause: {report['explanation']}\n")
    print("-" * 70 + "\nDECISION\n" + "-" * 70)
    print(f"Action: {report['decision']['action']}\nReason: {report['decision']['reason']}\n")
    print("-" * 70 + "\nMETRICS\n" + "-" * 70)
    print(f"MTTD: {report['metrics']['mttd']}\nResolution Time: {report['metrics']['resolution_time']}\nFalse Alert: {'Yes' if report['metrics']['false_alert'] else 'No'}\n")
    print("-" * 70 + "\nEXECUTION\n" + "-" * 70)
    print(report['action_result'])
    print("=" * 70)

def main():
    # Initialize Agent
    agent = IncidentResponseAgent()
    
    # Path configuration
    telemetry_file = "telemetry/memory_leak.json" 
    
    print(f"--- STARTING ANALYSIS FOR: {telemetry_file} ---")

    # Step 1: Load
    telemetry_data = load_telemetry(telemetry_file)
    if not telemetry_data: return

    # Step 2: Agent Execution
    report = agent.run_cycle(telemetry_data)

    # Step 3: Print Report
    print_report(report)

if __name__ == "__main__":
    main()