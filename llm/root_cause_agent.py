"""
root_cause_agent.py

Simulates an LLM-based agent that analyzes incident data to find the root cause.
In a real scenario, this would call OpenAI/Anthropic/Gemini APIs.
"""

import random

def explain_root_cause(incident_type):
    """
    Simulates an LLM analysis of the incident.
    
    Args:
        incident_type (str): The type of incident detected (e.g., MEMORY_LEAK)
        
    Returns:
        tuple: (explanation_text, confidence_score)
    """
    
    if incident_type == "MEMORY_LEAK":
        explanation = (
            "Analysis of heap dumps indicates a steady accumulation of "
            "unreferenced objects in the user session cache. "
            "Suspected cause: Circular reference in the SessionManager class."
        )
        # Simulate varying confidence
        confidence = 0.95
        
    elif incident_type == "API_TIMEOUT":
        explanation = (
            "Trace analysis shows 95th percentile latency exceeding 2000ms "
            "on the /payment endpoint. Database lock contention detected "
            "on 'transactions' table during high write throughput."
        )
        confidence = 0.92
        
    elif incident_type == "DISK_FULL":
        explanation = (
            "Log rotation failure detected in /var/log/application. "
            "Debug logs are consuming 45GB of space. "
            "The cleanup cron job failed to execute."
        )
        confidence = 0.98
        
    elif incident_type == "NO_INCIDENT":
        explanation = "System metrics are within normal operating ranges. No anomalies detected."
        confidence = 1.0
        
    else:
        explanation = "The system is behaving erratically, but the specific pattern is not recognized in the knowledge base."
        confidence = 0.4
    
    return explanation, confidence
