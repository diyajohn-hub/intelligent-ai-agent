"""
metrics.py

Helper utilities for incident response metrics and alert classification.

This module provides simple, self-contained functions for calculating
detection metrics and identifying false alerts in the incident response system.
"""


def calculate_mttd(timestamps):
    """
    Calculate Mean Time To Detection (MTTD) for incidents.
    
    Args:
        timestamps (list): List of timestamp strings from telemetry data
    
    Returns:
        str: Human-readable MTTD string
    
    Note:
        For hackathon/demo purposes, this returns a simulated value.
        In production, this would analyze actual incident start vs detection times
        by parsing timestamps and calculating the time difference between
        when the incident began and when it was detected by the system.
        Handles empty or invalid input gracefully.
    """
    if not timestamps or len(timestamps) == 0:
        return "N/A (no data available)"
    
    if len(timestamps) == 1:
        return "< 1 minute (single data point)"
    
    incident_count = len(timestamps)
    
    if incident_count < 5:
        return "~2 minutes (estimated)"
    elif incident_count < 10:
        return "~3 minutes (estimated)"
    else:
        return "~5 minutes (estimated)"


def is_false_alert(incident_type):
    """
    Determine if an incident is a false alert.
    
    Args:
        incident_type (str): The type of incident detected
    
    Returns:
        bool: True if the incident is a false alert, False otherwise
    
    Purpose:
        This metric helps reduce alert fatigue by identifying and suppressing
        false positives that would otherwise distract engineers from real issues.
    
    False Alert Criteria:
        - "NO_INCIDENT": System detected no real issue (transient anomaly)
        - None or empty string: Invalid detection
    """
    if incident_type is None or incident_type == "":
        return True
    
    if incident_type == "NO_INCIDENT":
        return True
    
    return False


def estimate_resolution_time(action):
    """
    Estimate time to resolve an incident based on action type.
    
    Args:
        action (str): The action type (AUTO_FIX, HUMAN_APPROVAL, ESCALATE, NO_ACTION)
    
    Returns:
        str: Estimated resolution time (simulated for hackathon demo)
    
    Note:
        This is a simulated metric for demonstration purposes.
        In production, this would be based on historical incident data.
    """
    resolution_times = {
        "AUTO_FIX": "~2 minutes (automated)",
        "HUMAN_APPROVAL": "~15 minutes (awaiting approval)",
        "ESCALATE": "~30 minutes (manual intervention)",
        "NO_ACTION": "0 minutes (no action required)"
    }
    
    return resolution_times.get(action, "Unknown (manual review required)")