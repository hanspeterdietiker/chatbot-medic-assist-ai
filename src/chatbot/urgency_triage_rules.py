
# ---------------------------------------------------------------------------
# Níveis de urgência (B05)
# ---------------------------------------------------------------------------
URGENCIA_BAIXA = "baixa"
URGENCIA_PRIORITARIO = "prioritario"
URGENCIA_EMERGENCIA = "emergencia"

# ---------------------------------------------------------------------------
# Áreas recomendadas
# ---------------------------------------------------------------------------
AREA_PRONTO_SOCORRO = "Pronto-Socorro"
AREA_CARDIOLOGIA = "Cardiologia / Pronto-Socorro"
AREA_NEUROLOGIA = "Neurologia / Pronto-Socorro"
AREA_OBSTETRICIA = "Obstetrícia / Pronto-Socorro"
AREA_ORTOPEDIA = "Ortopedia / Pronto Atendimento"
AREA_PNEUMOLOGIA = "Clínica Médica / Pneumologia"
AREA_PEDIATRIA = "Pediatria"
AREA_ENDOCRINOLOGIA = "Clínica Médica / Endocrinologia"
AREA_DERMATOLOGIA = "Dermatologia / Clínica Médica"
AREA_CLINICA_MEDICA = "Clínica Médica"

# ---------------------------------------------------------------------------
# Tabela de regras: (keywords, area, urgencia)
# Ordem importa — regras mais graves primeiro.
# ---------------------------------------------------------------------------
_CONDITION_RULES: list[tuple[tuple[str, ...], str, str]] = [
    # Neurológico — sempre emergência
    (
        ("stroke", "neurological", "avc", "neurologico"),
        AREA_NEUROLOGIA,
        URGENCIA_EMERGENCIA,
    ),
    # Cardíaco — prioritário (emergência capturada pelo check de sintomas abaixo)
    (
        ("heart", "chest pain", "cardiac", "coração", "peito", "cardíaco"),
        AREA_CARDIOLOGIA,
        URGENCIA_PRIORITARIO,
    ),
    # Gestação — sempre emergência
    (
        ("pregnancy", "gravidez", "gestacao", "gestação", "obstetr"),
        AREA_OBSTETRICIA,
        URGENCIA_EMERGENCIA,
    ),
    # Trauma / fratura — prioritário
    (
        ("fracture", "trauma", "fratura"),
        AREA_ORTOPEDIA,
        URGENCIA_PRIORITARIO,
    ),
    # Respiratório / infecção — baixa (área varia por idade; tratado em apply_rules)
    (
        ("flu", "respiratory", "infection", "gripe", "respirar", "respiratorio", "respiratório"),
        AREA_PNEUMOLOGIA,
        URGENCIA_BAIXA,
    ),
    # Metabólico / diabetes — prioritário
    (
        ("diabetes", "glucose", "glicose", "glicemia"),
        AREA_ENDOCRINOLOGIA,
        URGENCIA_PRIORITARIO,
    ),
    # Dermatológico — baixa
    (
        ("skin", "pele", "dermat"),
        AREA_DERMATOLOGIA,
        URGENCIA_BAIXA,
    ),
]

# ---------------------------------------------------------------------------
# Regras de agravamento por sintomas (B05)
# Elevam o nivel_urgencia independente da condição principal.
# ---------------------------------------------------------------------------
def _escalate_urgency(patient_data: dict, base_urgency: str) -> str:
    """Eleva a urgência com base em sintomas críticos."""
    if not patient_data["is_conscious"]:
        return URGENCIA_EMERGENCIA
    if patient_data["has_difficulty_breathing"]:
        return URGENCIA_EMERGENCIA
    if patient_data["has_intense_pain"] and base_urgency == URGENCIA_BAIXA:
        return URGENCIA_PRIORITARIO
    return base_urgency


def apply_rules(patient_data: dict) -> tuple[str, str]:
    """
    Aplica as regras de mapeamento e retorna (area_recomendada, nivel_urgencia).

    Critérios de aceite B05:
      - baixa     : condição não urgente, sem sintomas agravantes
      - prioritario: condição moderada ou sintoma de dor intensa
      - emergencia : inconsciência, dificuldade respiratória ou condição crítica
    """
    condition = patient_data["primary_condition"].lower()
    age = patient_data["age"]

    # Sintomas críticos imediatos — área genérica, emergência
    if not patient_data["is_conscious"] or patient_data["has_difficulty_breathing"]:
        return AREA_PRONTO_SOCORRO, URGENCIA_EMERGENCIA

    # Percorre as regras por condição
    for keywords, area, urgency in _CONDITION_RULES:
        if any(keyword in condition for keyword in keywords):
            # Ajuste de área por faixa etária para respiratório
            if area == AREA_PNEUMOLOGIA and age < 12:
                area = AREA_PEDIATRIA
            urgency = _escalate_urgency(patient_data, urgency)
            return area, urgency

    # Sem correspondência — clínica geral
    urgency = _escalate_urgency(patient_data, URGENCIA_BAIXA)
    return AREA_CLINICA_MEDICA, urgency
