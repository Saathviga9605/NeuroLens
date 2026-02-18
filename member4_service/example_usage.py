"""
Example usage script for Member 4 Service.

This script demonstrates how to interact with the Behavioral Intelligence 
& Multimodal Fusion Engine API.
"""

import requests
import json
from typing import Dict


# Service endpoint
BASE_URL = "http://localhost:8000/api/v1"


def check_health() -> Dict:
    """Check service health."""
    response = requests.get(f"{BASE_URL}/health")
    return response.json()


def analyze_normal_behavior() -> Dict:
    """Example: Analyze normal behavioral pattern."""
    normal_behavior = {
        "typing_speed": 3.5,
        "error_rate": 0.15,
        "backspace_frequency": 0.25,
        "pause_variability": 1.2,
        "sleep_duration": 7.0,
        "sleep_drift": 0.5,
        "app_usage_entropy": 2.3,
        "session_frequency": 15.0,
        "activity_regularity": 0.75
    }
    
    response = requests.post(
        f"{BASE_URL}/behavior/analyze",
        json=normal_behavior
    )
    return response.json()


def analyze_anomalous_behavior() -> Dict:
    """Example: Analyze anomalous behavioral pattern."""
    anomalous_behavior = {
        "typing_speed": 1.8,  # Much slower
        "error_rate": 0.45,    # High error rate
        "backspace_frequency": 0.62,  # Lots of corrections
        "pause_variability": 3.5,  # Erratic typing
        "sleep_duration": 4.2,  # Sleep deprived
        "sleep_drift": -4.5,    # Irregular sleep schedule
        "app_usage_entropy": 4.1,  # Chaotic app usage
        "session_frequency": 6.0,  # Reduced activity
        "activity_regularity": 0.32  # Irregular patterns
    }
    
    response = requests.post(
        f"{BASE_URL}/behavior/analyze",
        json=anomalous_behavior
    )
    return response.json()


def compute_fusion_low_risk() -> Dict:
    """Example: Multimodal fusion with low overall risk."""
    low_risk_scores = {
        "sentiment_drift": 0.25,
        "voice_stress": 0.18,
        "behavioral_anomaly": 0.22
    }
    
    response = requests.post(
        f"{BASE_URL}/fusion/score",
        json=low_risk_scores
    )
    return response.json()


def compute_fusion_high_risk() -> Dict:
    """Example: Multimodal fusion with high overall risk."""
    high_risk_scores = {
        "sentiment_drift": 0.82,
        "voice_stress": 0.75,
        "behavioral_anomaly": 0.88
    }
    
    response = requests.post(
        f"{BASE_URL}/fusion/score",
        json=high_risk_scores
    )
    return response.json()


def compute_fusion_mixed_signals() -> Dict:
    """Example: Multimodal fusion with mixed signals."""
    mixed_scores = {
        "sentiment_drift": 0.65,
        "voice_stress": 0.28,
        "behavioral_anomaly": 0.71
    }
    
    response = requests.post(
        f"{BASE_URL}/fusion/score",
        json=mixed_scores,
        params={"fusion_strategy": "weighted"}
    )
    return response.json()


def test_adaptive_fusion() -> Dict:
    """Example: Use adaptive fusion engine."""
    scores = {
        "sentiment_drift": 0.55,
        "voice_stress": 0.42,
        "behavioral_anomaly": 0.68
    }
    
    response = requests.post(
        f"{BASE_URL}/fusion/score",
        json=scores,
        params={
            "fusion_strategy": "geometric",
            "use_adaptive": True
        }
    )
    return response.json()


def main():
    """Run example demonstrations."""
    print("=" * 70)
    print("Member 4 Service - Example Usage")
    print("=" * 70)
    
    # Health check
    print("\n1. Health Check")
    print("-" * 70)
    health = check_health()
    print(json.dumps(health, indent=2))
    
    # Normal behavior analysis
    print("\n2. Analyze Normal Behavior")
    print("-" * 70)
    normal_result = analyze_normal_behavior()
    print(json.dumps(normal_result, indent=2))
    print(f"Risk Flag: {normal_result['risk_flag']}")
    print(f"Anomaly Score: {normal_result['behavioral_anomaly_score']:.3f}")
    
    # Anomalous behavior analysis
    print("\n3. Analyze Anomalous Behavior")
    print("-" * 70)
    anomalous_result = analyze_anomalous_behavior()
    print(json.dumps(anomalous_result, indent=2))
    print(f"Risk Flag: {anomalous_result['risk_flag']}")
    print(f"Anomaly Score: {anomalous_result['behavioral_anomaly_score']:.3f}")
    
    # Low risk fusion
    print("\n4. Multimodal Fusion - Low Risk")
    print("-" * 70)
    low_risk = compute_fusion_low_risk()
    print(json.dumps(low_risk, indent=2))
    print(f"Alert Level: {low_risk['alert_level']}")
    print(f"Overall Risk: {low_risk['overall_risk_score']:.3f}")
    
    # High risk fusion
    print("\n5. Multimodal Fusion - High Risk")
    print("-" * 70)
    high_risk = compute_fusion_high_risk()
    print(json.dumps(high_risk, indent=2))
    print(f"Alert Level: {high_risk['alert_level']}")
    print(f"Overall Risk: {high_risk['overall_risk_score']:.3f}")
    
    # Mixed signals fusion
    print("\n6. Multimodal Fusion - Mixed Signals")
    print("-" * 70)
    mixed = compute_fusion_mixed_signals()
    print(json.dumps(mixed, indent=2))
    print(f"Dominant Factor: {mixed['dominant_factor']}")
    print(f"Alert Level: {mixed['alert_level']}")
    
    # Adaptive fusion
    print("\n7. Adaptive Fusion Engine")
    print("-" * 70)
    adaptive = test_adaptive_fusion()
    print(json.dumps(adaptive, indent=2))
    
    print("\n" + "=" * 70)
    print("Examples completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to service.")
        print("Make sure the service is running on http://localhost:8004")
        print("\nStart the service with: python main.py")
    except Exception as e:
        print(f"Error: {e}")
