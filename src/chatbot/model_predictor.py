"""
Preditor de triagem integrado ao modelo treinado (B21).

Carrega o melhor algoritmo (DT ou RF) de models/, prediz as doenças mais
prováveis (top-N via predict_proba), aplica regras de hábitos de vida
(álcool/fumo) e deriva área e urgência da doença #1 com as regras clínicas.

Retorno de predict_triage:
    (doencas_top, area_recomendada, nivel_urgencia, fonte)
onde doencas_top é uma lista de (nome_doenca, probabilidade) já re-ranqueada.
"""

import json
import pathlib

try:
    import joblib
    import pandas as pd
except ImportError:
    joblib = None
    pd = None

from .patient_encoder import encode_patient_data, FEATURE_ORDER
from .recommended_area_rules import (
    AREA_PRONTO_SOCORRO,
    apply_area_rules,
)
from .urgency_triage_rules import (
    URGENCIA_EMERGENCIA,
    apply_urgency_rules,
    apply_rules,
    is_immediate_emergency,
)
from .lifestyle_rules import apply_lifestyle_reranking, escalate_for_lifestyle

ROOT_DIR       = pathlib.Path(__file__).parent.parent.parent
MODELS_DIR     = ROOT_DIR / "models"
ENCODING_MAPS  = ROOT_DIR / "dataset" / "processed" / "encoding_maps.json"
METADATA_FILE  = MODELS_DIR / "model_metadata.json"

DEFAULT_TOP_K = 5

# Rótulos legíveis dos algoritmos para exibição ao paciente (B22)
_ALGO_DISPLAY = {
    "decision_tree": "Árvore de Decisão",
    "random_forest": "Random Forest",
}

# Cache dos artefatos carregados — evita releitura a cada predição na mesma sessão
_models_cache: dict | None = None
_maps_cache: dict | None = None
_metadata_cache: dict | None = None


def _models_available() -> bool:
    """Verifica se os artefatos de treinamento existem."""
    return METADATA_FILE.exists() and joblib is not None


def _load_resources() -> tuple[dict, dict, object]:
    """Carrega metadados, mapas de codificação e o modelo de doença."""
    global _models_cache, _maps_cache, _metadata_cache

    if _metadata_cache is None:
        with open(METADATA_FILE, encoding="utf-8") as fh:
            _metadata_cache = json.load(fh)
        with open(ENCODING_MAPS, encoding="utf-8") as fh:
            _maps_cache = json.load(fh)

        algo = _metadata_cache["best_algorithm"]
        _models_cache = {
            "disease": joblib.load(MODELS_DIR / f"{algo}_disease.joblib"),
            "algo":    algo,
        }

    return _metadata_cache, _maps_cache, _models_cache["disease"]


def _decode_disease(encoded_value: int, maps: dict) -> str:
    """Converte código numérico da doença de volta ao nome legível."""
    inverted = {v: k for k, v in maps["disease"].items()}
    return inverted[int(encoded_value)]


def _ranked_diseases(model, maps: dict, features) -> list[tuple[str, float]]:
    """Lista (doença, probabilidade) ordenada do mais provável ao menos."""
    proba = model.predict_proba(features)[0]
    pairs = [
        (_decode_disease(cls, maps), float(p))
        for cls, p in zip(model.classes_, proba)
    ]
    pairs.sort(key=lambda item: item[1], reverse=True)
    return pairs


def predict_triage(patient_data: dict) -> tuple[list[tuple[str, float]], str, str, str]:
    """
    Retorna (doencas_top, area_recomendada, nivel_urgencia, fonte).

    fonte: "modelo_ia (...)" | "regras_seguranca" | "regras_fallback"
    """
    # Camada 1 — emergência imediata: inconsciência, dificuldade respiratória
    # ou qualquer sinal de alerta 🔴 (sangramento, convulsão, etc.). A segurança
    # força Pronto-Socorro + emergência, mas as doenças prováveis ainda são
    # exibidas como apoio (o modelo roda normalmente quando disponível).
    emergency = is_immediate_emergency(patient_data)

    # Fallback gracioso se modelos não foram treinados — sem doença prevista
    if not _models_available():
        if emergency:
            return [], AREA_PRONTO_SOCORRO, URGENCIA_EMERGENCIA, "regras_seguranca"
        area, urgency = apply_rules({**patient_data, "primary_condition": ""})
        return [], area, urgency, "regras_fallback"

    metadata, maps, model = _load_resources()
    top_k = metadata.get("top_k", DEFAULT_TOP_K)

    # Codifica e prediz as doenças prováveis
    features = pd.DataFrame([encode_patient_data(patient_data)], columns=FEATURE_ORDER)
    ranked = _ranked_diseases(model, maps, features)

    # Camada de hábitos — re-ranqueia o top-N (fumo/álcool)
    ranked = apply_lifestyle_reranking(ranked, patient_data)
    top = ranked[:top_k]
    top1_disease = top[0][0]

    # Em emergência, mantém as doenças de apoio mas a área/urgência são ditadas
    # pela regra de segurança (não pela doença #1).
    if emergency:
        return top, AREA_PRONTO_SOCORRO, URGENCIA_EMERGENCIA, "regras_seguranca"

    # Deriva área da doença #1 (apply_area_rules já trata override pediátrico)
    area = apply_area_rules(top1_disease, int(patient_data["age"]))

    # Urgência: base da doença #1 + escalada por sintomas + escalada por hábitos
    urgency = apply_urgency_rules({**patient_data, "primary_condition": top1_disease})
    urgency = escalate_for_lifestyle(urgency, top1_disease, patient_data)

    algo_name = _ALGO_DISPLAY.get(_models_cache["algo"], _models_cache["algo"])
    return top, area, urgency, f"modelo_ia ({algo_name})"


def get_algorithm_display_name() -> str:
    """Retorna nome legível do algoritmo em uso (para exibição B22)."""
    if not _models_available():
        return "Regras clínicas"
    metadata, _, _ = _load_resources()
    return _ALGO_DISPLAY.get(metadata["best_algorithm"], metadata["best_algorithm"])
