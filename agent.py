from detector.incident_detector import IncidentDetector
from llm.root_cause_agent import explain_root_cause
from decision.decision_engine import make_decision
from actions.remediation import apply_fix
from utils.metrics import calculate_mttd, is_false_alert, estimate_resolution_time

class IncidentResponseAgent:
    def __init__(self, model_name="LLM-Model"):
        self.model = model_name
        self.detector = IncidentDetector()

    def run_cycle(self, telemetry_data):
        """
        Executes the full incident response lifecycle:
        Detect -> Analyze -> Decide -> Act -> Report
        """
        # Step 1: Detect
        detection_result = self.detector.analyze(telemetry_data)
        if not detection_result:
            return "No telemetry data to analyze."
            
        incident_raw = detection_result['incident']
        
        # Mapping detector output to system codes
        type_mapping = {
            "Memory Leak": "MEMORY_LEAK",
            "Disk Full": "DISK_FULL",
            "API Timeout": "API_TIMEOUT",
            "False Positive": "NO_INCIDENT",
            "None": "NO_INCIDENT"
        }
        incident_type = type_mapping.get(incident_raw, "UNKNOWN")

        # Step 2: LLM Analysis
        explanation, confidence = explain_root_cause(incident_type)

        # Step 3: Decision
        decision = make_decision(incident_type, confidence)

        # Step 4: Metrics
        # Assuming telemetry_data is a list of dicts with 'timestamp'
        timestamps = [entry.get("timestamp") for entry in telemetry_data if "timestamp" in entry]
        mttd = calculate_mttd(timestamps)
        false_alert = is_false_alert(incident_type)
        resolution_time = estimate_resolution_time(decision['action'])

        # Step 5: Execute Remediation
        action_result = apply_fix(decision['action'])

        # Step 6: Construct Report
        report = {
            "incident_type": incident_type,
            "decision": decision,
            "explanation": explanation,
            "confidence": confidence,
            "metrics": {
                "mttd": mttd,
                "false_alert": false_alert,
                "resolution_time": resolution_time
            },
            "action_result": action_result
        }

        return report

    def analyze_with_llm(self, detector_output):
        """
        Legacy method kept for backward compatibility if needed, 
        but logic is now integrated into run_cycle.
        """
        incident_type = detector_output['incident']
        reason = detector_output['reason']
        
        llm_explanation = f"AI ROOT CAUSE ANALYSIS: Based on the {incident_type} flag, " \
                          f"the system detected {reason}. This is likely due to a " \
                          f"resource leak in the production environment."
        
        return llm_explanation
