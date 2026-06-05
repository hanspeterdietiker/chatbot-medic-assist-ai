from .conversation import collect_patient_data, display_result, build_triage_summary
from .messages import BOAS_VINDAS, ENCERRAMENTO, AVISO_EMERGENCIA, AVISO_RESULTADO
from .urgency_triage_rules import apply_rules, apply_urgency_rules, get_base_urgency
from .recommended_area_rules import apply_area_rules

__all__ = [
    "collect_patient_data",
    "display_result",
    "build_triage_summary",
    "apply_rules",
    "apply_urgency_rules",
    "get_base_urgency",
    "apply_area_rules",
    "BOAS_VINDAS",
    "ENCERRAMENTO",
    "AVISO_EMERGENCIA",
    "AVISO_RESULTADO",
]
