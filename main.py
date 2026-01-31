from detector.incident_detector import IncidentDetector
from agent import IncidentResponseAgent
import os

def main():
    # Initialize your parts
    detector = IncidentDetector()
    agent = IncidentResponseAgent()

    # List of telemetry files to check [cite: 5, 9]
    telemetry_files = [
        'telemetry/memory_leak.json',
        'telemetry/api_timeout.json',
        'telemetry/false_alert.json'
    ]

    print("--- STARTING INTELLIGENT INCIDENT AGENT ---")

    for file_path in telemetry_files:
        print(f"\n[STEP 1] Ingesting: {file_path}") [cite: 5]
        
        # 1. Run your detector logic (Decision Tree) 
        data = detector.load_telemetry(file_path)
        if not data:
            continue
            
        detection_result = detector.analyze(data)
        
        # 2. Print the reasoning for the action 
        print(f"[STEP 2] Detection Result: {detection_result['incident']}")
        print(f"[STEP 3] Action Taken: {detection_result['action']}") [cite: 7]
        
        # 3. Pass to Agent for LLM Root Cause Analysis 
        if detection_result['incident'] != "None" and detection_result['incident'] != "False Positive":
            ai_explanation = agent.analyze_with_llm(detection_result)
            print(f"[STEP 4] {ai_explanation}") [cite: 12]
        else:
            print("[STEP 4] System stable. No AI analysis needed.")

if __name__ == "__main__":
    main()