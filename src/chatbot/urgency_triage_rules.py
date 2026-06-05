from .recommended_area_rules import (
    apply_area_rules,
    AREA_PRONTO_SOCORRO,
    KEYWORDS_NEUROLOGICAL,
    KEYWORDS_PREGNANCY,
    KEYWORDS_APPENDICITIS,
    KEYWORDS_CARDIAC,
    KEYWORDS_FRACTURE,
    KEYWORDS_DIABETES,
    KEYWORDS_CANCER,
    KEYWORDS_RESPIRATORY,
    KEYWORDS_SKIN,
)

# ---------------------------------------------------------------------------
# Níveis de urgência (B05)
# ---------------------------------------------------------------------------
URGENCIA_BAIXA       = "baixa"
URGENCIA_PRIORITARIO = "prioritario"
URGENCIA_EMERGENCIA  = "emergencia"

# ---------------------------------------------------------------------------
# Tabela de regras: (keywords, urgencia_base)
# Usa as mesmas keyword constants de recommended_area_rules — fonte única de
# verdade. Adicionar keyword a uma constante aplica em ambas as tabelas.
# ---------------------------------------------------------------------------
_URGENCY_RULES: list[tuple[tuple[str, ...], str]] = [
    (KEYWORDS_NEUROLOGICAL,  URGENCIA_EMERGENCIA),
    (KEYWORDS_PREGNANCY,     URGENCIA_EMERGENCIA),
    (KEYWORDS_APPENDICITIS,  URGENCIA_EMERGENCIA),
    (KEYWORDS_CARDIAC,       URGENCIA_PRIORITARIO),
    (KEYWORDS_FRACTURE,      URGENCIA_PRIORITARIO),
    (KEYWORDS_DIABETES,      URGENCIA_PRIORITARIO),
    (KEYWORDS_CANCER,        URGENCIA_PRIORITARIO),
    (KEYWORDS_RESPIRATORY,   URGENCIA_BAIXA),
    (KEYWORDS_SKIN,          URGENCIA_BAIXA),
]

# ---------------------------------------------------------------------------
# Agravamento por sintomas (B05)
# ---------------------------------------------------------------------------
def _escalate_urgency(patient_data: dict, base_urgency: str) -> str:
    """Eleva a urgência com base em sintomas críticos."""
    # Inconsciência e dificuldade respiratória já tratadas antes de chamar esta
    # função — não precisam ser verificadas novamente aqui.
    if patient_data["has_intense_pain"] and base_urgency == URGENCIA_BAIXA:
        return URGENCIA_PRIORITARIO
    return base_urgency


def get_base_urgency(condition: str) -> str:
    """Retorna a urgência base para uma condição, sem escalada por sintomas."""
    normalized = condition.lower().strip()
    for keywords, urgency in _URGENCY_RULES:
        if any(keyword in normalized for keyword in keywords):
            return urgency
    return URGENCIA_BAIXA


def apply_urgency_rules(patient_data: dict) -> str:
    """
    Retorna o nivel_urgencia para os dados do paciente.

    Critérios de aceite B05:
      - baixa     : condição não urgente, sem sintomas agravantes
      - prioritario: condição moderada ou sintoma de dor intensa
      - emergencia : inconsciência, dificuldade respiratória ou condição crítica
    """
    if not patient_data["is_conscious"] or patient_data["has_difficulty_breathing"]:
        return URGENCIA_EMERGENCIA

    base = get_base_urgency(patient_data["primary_condition"])
    return _escalate_urgency(patient_data, base)


def apply_rules(patient_data: dict) -> tuple[str, str]:
    """
    Retorna (area_recomendada, nivel_urgencia) para os dados do paciente.
    Combina apply_area_rules + apply_urgency_rules.
    """
    if not patient_data["is_conscious"] or patient_data["has_difficulty_breathing"]:
        return AREA_PRONTO_SOCORRO, URGENCIA_EMERGENCIA

    area    = apply_area_rules(patient_data["primary_condition"], patient_data["age"])
    urgency = apply_urgency_rules(patient_data)
    return area, urgency
