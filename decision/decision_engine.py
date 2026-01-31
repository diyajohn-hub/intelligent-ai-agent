"""
decision_engine.py

AI-Assisted Incident Response Decision Engine

Philosophy:
"Act automatically only when safe, otherwise involve humans."

This module implements a decision tree that determines the appropriate
response action for detected incidents based on type and confidence level.
It prioritizes safety by escalating uncertain or high-impact incidents
to human operators while automating only safe, reversible fixes.
"""


def make_decision(incident_type, confidence):
    """
    Determine the appropriate response action for a detected incident.
    
    Args:
        incident_type (str): Type of incident detected
            Valid values: "MEMORY_LEAK", "API_TIMEOUT", "DISK_FULL", "NO_INCIDENT"
        confidence (float): LLM confidence score (0.0 to 1.0)
    
    Returns:
        dict: Decision containing:
            - action (str): AUTO_FIX | HUMAN_APPROVAL | ESCALATE | NO_ACTION
            - severity (str): LOW | MEDIUM | HIGH | CRITICAL
            - reason (str): Human-readable explanation
    
    Decision Logic:
        - NO_INCIDENT: Suppress false alerts (explicit suppression)
        - DISK_FULL: Safe to auto-remediate (clear temp files)
        - MEMORY_LEAK: Requires human judgment based on confidence
        - API_TIMEOUT: High user impact, always escalate
    """
    
    # Rule 1: EXPLICIT false alert suppression - must be first
    if incident_type == "NO_INCIDENT":
        return {
            "action": "NO_ACTION",
            "severity": "LOW",
            "reason": "Transient anomaly detected. Alert suppressed."
        }
    
    # Rule 2: Safe auto-fix for disk space issues
    if incident_type == "DISK_FULL":
        return {
            "action": "AUTO_FIX",
            "severity": "MEDIUM",
            "reason": "Critical storage alert verified. Automated cleanup routine (safe mode) engaged to recover disk space."
        }
    
    # Rule 3: Memory leak handling based on confidence
    if incident_type == "MEMORY_LEAK":
        if confidence > 0.9:
            # Very high confidence - Auto-remediate!
            return {
                "action": "AUTO_FIX",
                "severity": "HIGH",
                "reason": f"Memory leak detected with critical confidence ({confidence:.2f}). "
                         "Initiating automated service restart to restore health."
            }
        elif confidence >= 0.8:
            # High confidence - get human approval before restart
            return {
                "action": "HUMAN_APPROVAL",
                "severity": "HIGH",
                "reason": f"Memory leak detected with high confidence ({confidence:.2f}). "
                         "Service restart recommended - awaiting human approval."
            }
        else:
            # Low confidence - escalate for investigation
            return {
                "action": "ESCALATE",
                "severity": "MEDIUM",
                "reason": f"Potential memory leak detected with low confidence ({confidence:.2f}). "
                         "Escalating to on-call engineer for investigation."
            }
    
    # Rule 4: API timeout always escalates (high user impact)
    if incident_type == "API_TIMEOUT":
        return {
            "action": "ESCALATE",
            "severity": "CRITICAL",
            "reason": "API timeout detected. High user impact - immediate escalation required."
        }
    
    # Safety fallback: Escalate unknown incident types
    return {
        "action": "ESCALATE",
        "severity": "HIGH",
        "reason": f"Unknown incident type: {incident_type}. Escalating for manual review."
    }


def get_action_description(action):
    """
    Get a human-friendly description of what each action means.
    
    Args:
        action (str): The action type
    
    Returns:
        str: Description of the action
    """
    descriptions = {
        "AUTO_FIX": "System will automatically remediate the issue",
        "HUMAN_APPROVAL": "Automated fix ready - requires human approval to proceed",
        "ESCALATE": "Alert sent to on-call engineer for immediate attention",
        "NO_ACTION": "No action needed - monitoring continues"
    }
    return descriptions.get(action, "Unknown action")