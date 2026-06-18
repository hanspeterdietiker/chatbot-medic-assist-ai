from .conversation import collect_patient_data, display_result, build_triage_summary
from .messages import BOAS_VINDAS, ENCERRAMENTO, AVISO_EMERGENCIA, AVISO_RESULTADO
from .urgency_triage_rules import apply_rules, apply_urgency_rules, get_base_urgency
from .recommended_area_rules import apply_area_rules
from .model_predictor import predict_triage, get_algorithm_display_name
from .patient_encoder import encode_patient_data
from .lifestyle_rules import apply_lifestyle_reranking, escalate_for_lifestyle, lifestyle_factors
from .terminal_ui import show_loading, show_welcome, urgency_style, get_console

__all__ = [
    "collect_patient_data",
    "display_result",
    "build_triage_summary",
    "apply_rules",
    "apply_urgency_rules",
    "get_base_urgency",
    "apply_area_rules",
    "predict_triage",
    "get_algorithm_display_name",
    "encode_patient_data",
    "apply_lifestyle_reranking",
    "escalate_for_lifestyle",
    "lifestyle_factors",
    "show_loading",
    "show_welcome",
    "urgency_style",
    "get_console",
    "BOAS_VINDAS",
    "ENCERRAMENTO",
    "AVISO_EMERGENCIA",
    "AVISO_RESULTADO",
]
