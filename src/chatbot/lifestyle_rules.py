"""
Regras de hábitos de vida (álcool e tabagismo) — camada pós-modelo.

O dataset de treino não contém colunas de álcool/fumo, então esses hábitos
NÃO são features do modelo. Em vez disso, são coletados no chatbot e aplicados
aqui como ajustes clínicos documentados sobre a saída do modelo:

  1. Re-ranqueamento do top-N de doenças prováveis (boost para categorias de
     risco associadas ao hábito).
  2. Escalada de urgência quando o hábito está associado à doença prevista.

Racional clínico (simplificado, para apoio à triagem — não diagnóstico):
  - Tabagismo  → maior risco respiratório e cardiovascular.
  - Álcool     → maior risco hepático e gastrointestinal.
"""

from .recommended_area_rules import KEYWORDS_RESPIRATORY, KEYWORDS_CARDIAC
from .urgency_triage_rules import (
    URGENCIA_BAIXA,
    URGENCIA_PRIORITARIO,
    URGENCIA_EMERGENCIA,
)

# Categorias de risco por hábito (keywords casadas no nome da doença)
SMOKING_RISK_KEYWORDS: tuple[str, ...] = KEYWORDS_RESPIRATORY + KEYWORDS_CARDIAC
ALCOHOL_RISK_KEYWORDS: tuple[str, ...] = (
    "liver", "hepat", "cirrhosis", "pancrea", "gastr", "ulcer",
    "esophageal", "cholecyst",
)

# Fator de boost aplicado à probabilidade de doenças de risco
BOOST_FACTOR = 1.6

_URGENCY_ORDER = {
    URGENCIA_BAIXA:       0,
    URGENCIA_PRIORITARIO: 1,
    URGENCIA_EMERGENCIA:  2,
}
_ORDER_TO_URGENCY = {v: k for k, v in _URGENCY_ORDER.items()}


def _matches(disease: str, keywords: tuple[str, ...]) -> bool:
    """True se alguma keyword aparece no nome da doença (case-insensitive)."""
    normalized = disease.lower()
    return any(kw in normalized for kw in keywords)


def apply_lifestyle_reranking(
    disease_probs: list[tuple[str, float]],
    patient_data: dict,
) -> list[tuple[str, float]]:
    """
    Re-ranqueia (doença, probabilidade) elevando categorias de risco do hábito.

    Não altera nada quando o paciente não fuma nem bebe. Probabilidades são
    re-normalizadas para somar 1 após o boost.
    """
    smokes = patient_data.get("smokes", False)
    drinks = patient_data.get("drinks_alcohol", False)
    if not smokes and not drinks:
        return list(disease_probs)

    boosted: list[tuple[str, float]] = []
    for name, prob in disease_probs:
        factor = 1.0
        if smokes and _matches(name, SMOKING_RISK_KEYWORDS):
            factor = BOOST_FACTOR
        if drinks and _matches(name, ALCOHOL_RISK_KEYWORDS):
            factor = BOOST_FACTOR
        boosted.append((name, prob * factor))

    total = sum(p for _, p in boosted) or 1.0
    boosted = [(name, prob / total) for name, prob in boosted]
    boosted.sort(key=lambda item: item[1], reverse=True)
    return boosted


def escalate_for_lifestyle(urgency: str, disease: str, patient_data: dict) -> str:
    """
    Eleva a urgência em 1 nível quando o hábito está associado à doença.

    Ex.: fumante com doença respiratória, ou etilista com doença hepática.
    Limitada a `emergencia` (não ultrapassa o teto).
    """
    bump = False
    if patient_data.get("smokes") and _matches(disease, SMOKING_RISK_KEYWORDS):
        bump = True
    if patient_data.get("drinks_alcohol") and _matches(disease, ALCOHOL_RISK_KEYWORDS):
        bump = True

    if not bump:
        return urgency

    new_level = min(_URGENCY_ORDER.get(urgency, 0) + 1, 2)
    return _ORDER_TO_URGENCY[new_level]


def lifestyle_factors(patient_data: dict) -> list[str]:
    """Rótulos legíveis dos hábitos informados (para exibição ao paciente)."""
    factors: list[str] = []
    if patient_data.get("smokes"):
        factors.append("Tabagismo")
    if patient_data.get("drinks_alcohol"):
        factors.append("Consumo de álcool")
    return factors
