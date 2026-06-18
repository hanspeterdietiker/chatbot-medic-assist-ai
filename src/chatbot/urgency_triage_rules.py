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
# Sinais de alerta coletados na etapa "Sinais de alerta" (passo 3).
# Mescla de sinais críticos (🔴 emergência) e de urgência (🟡 prioritário).
# Fonte única de verdade para o mapeamento rótulo→flag em conversation.py.
# ---------------------------------------------------------------------------
# Sinais 🔴 — risco de vida → Pronto-Socorro / emergência imediata.
EMERGENCY_SIGNAL_FLAGS: tuple[str, ...] = (
    "has_severe_bleeding",      # Sangramento intenso
    "has_seizure",              # Convulsão
    "has_sudden_confusion",     # Confusão mental súbita
    "has_unilateral_weakness",  # Dormência/fraqueza em um lado do corpo
)
# Sinais 🟡 — elevam a urgência para no mínimo prioritário.
URGENCY_SIGNAL_FLAGS: tuple[str, ...] = (
    "has_persistent_vomiting",   # Vômito persistente
    "has_severe_abdominal_pain", # Dor abdominal forte
    "has_dizziness",             # Tontura
    "has_palpitations",          # Palpitações
)


def has_emergency_signal(patient_data: dict) -> bool:
    """True se algum sinal 🔴 (risco de vida) foi marcado."""
    return any(patient_data.get(flag, False) for flag in EMERGENCY_SIGNAL_FLAGS)


def has_urgency_signal(patient_data: dict) -> bool:
    """True se algum sinal 🟡 (urgência) foi marcado."""
    return any(patient_data.get(flag, False) for flag in URGENCY_SIGNAL_FLAGS)


def is_immediate_emergency(patient_data: dict) -> bool:
    """
    Camada de segurança: condições que exigem Pronto-Socorro imediato,
    independentemente da condição/doença prevista.

    Inconsciência, dificuldade respiratória ou qualquer sinal 🔴.
    """
    return (
        not patient_data["is_conscious"]
        or patient_data["has_difficulty_breathing"]
        or has_emergency_signal(patient_data)
    )

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
    """Eleva a urgência com base em sintomas e sinais de alerta 🟡."""
    # Inconsciência, dificuldade respiratória e sinais 🔴 já tratados antes de
    # chamar esta função — não precisam ser verificados novamente aqui.
    if base_urgency == URGENCIA_BAIXA and (
        patient_data["has_intense_pain"] or has_urgency_signal(patient_data)
    ):
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
    if is_immediate_emergency(patient_data):
        return URGENCIA_EMERGENCIA

    base = get_base_urgency(patient_data["primary_condition"])
    return _escalate_urgency(patient_data, base)


def apply_rules(patient_data: dict) -> tuple[str, str]:
    """
    Retorna (area_recomendada, nivel_urgencia) para os dados do paciente.
    Combina apply_area_rules + apply_urgency_rules.
    """
    if is_immediate_emergency(patient_data):
        return AREA_PRONTO_SOCORRO, URGENCIA_EMERGENCIA

    area    = apply_area_rules(patient_data["primary_condition"], patient_data["age"])
    urgency = apply_urgency_rules(patient_data)
    return area, urgency
