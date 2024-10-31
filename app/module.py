# app/your_module.py

import re

def calculate_risk_score(risk_scenario):
    """
    Calculates the risk score based on the risk scenario.

    Args:
        risk_scenario (str): The risk scenario description.

    Returns:
        str: A description of the risk level (e.g., "High Risk", "Low Risk").
    """
    if risk_scenario == "high-risk-scenario":
        return "High Risk"
    elif risk_scenario == "low-risk-scenario":
        return "Low Risk"
    else:
        return "Unknown Risk"

def validate_email(email):
    """
    Validates an email address using a simple regex pattern.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))
