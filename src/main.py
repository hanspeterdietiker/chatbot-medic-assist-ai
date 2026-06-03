"""Entry point do Medic Assist AI. Execute: python src/main.py"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from chatbot.conversation import collect_patient_data, display_result, build_triage_summary
from chatbot.urgency_triage_rules import apply_rules


def run() -> dict:
    patient_data = collect_patient_data()
    recommended_area, urgency_level = apply_rules(patient_data)
    display_result(patient_data, recommended_area, urgency_level)
    return build_triage_summary(patient_data, recommended_area, urgency_level)


if __name__ == "__main__":
    run()
