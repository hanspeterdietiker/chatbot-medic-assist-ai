"""
Codificador de dados do paciente para entrada do modelo (B21).

Converte o dict coletado pelo chatbot no vetor numérico esperado pelo modelo
de doença, na ordem de FEATURE_COLS (train_model.py):

    [age, gender, fever, cough, fatigue, difficulty_breathing,
     blood_pressure, cholesterol_level]

Usa os mesmos mapeamentos do treinamento (encoding_maps.json). Hábitos
(álcool/fumo) NÃO entram aqui — são aplicados como regras pós-modelo
(ver chatbot/lifestyle_rules.py).
"""

import json
import pathlib

ROOT_DIR      = pathlib.Path(__file__).parent.parent.parent
ENCODING_MAPS = ROOT_DIR / "dataset" / "processed" / "encoding_maps.json"

# Ordem das features — deve casar com FEATURE_COLS em train_model.py
FEATURE_ORDER = [
    "age", "gender", "fever", "cough", "fatigue",
    "difficulty_breathing", "blood_pressure", "cholesterol_level",
]

# Gênero do chatbot → rótulo do dataset (alinhado a encoding_maps.json)
GENDER_CHATBOT_TO_DATASET: dict[str, str] = {
    "Feminino":                      "Female",
    "Masculino":                     "Male",
    "Outro / Prefiro não informar":  "Female",  # default — dataset só tem Female/Male
}

# Níveis de saúde do chatbot (PT) → rótulo do dataset (Low/Normal/High)
HEALTH_LEVEL_TO_DATASET: dict[str, str] = {
    "baixa": "Low", "baixo": "Low", "low": "Low",
    "normal": "Normal",
    "alta": "High", "alto": "High", "high": "High",
    "não sei": "Normal", "nao sei": "Normal", "": "Normal",
}


def _load_encoding_maps() -> dict:
    """Carrega mapeamentos label→int gerados pelo encode_dataset.py."""
    with open(ENCODING_MAPS, encoding="utf-8") as fh:
        return json.load(fh)


def _yes_no(value: bool) -> str:
    """Converte bool do chatbot para o rótulo do dataset."""
    return "Yes" if value else "No"


def _health_level(value: str) -> str:
    """Normaliza o nível de pressão/colesterol para Low/Normal/High."""
    return HEALTH_LEVEL_TO_DATASET.get(str(value).strip().lower(), "Normal")


def encode_patient_data(patient_data: dict) -> list[int]:
    """
    Retorna o vetor numérico de features na ordem de FEATURE_ORDER.

    Usa encoding_maps.json para garantir a mesma codificação do treinamento.
    """
    maps = _load_encoding_maps()

    gender_label = GENDER_CHATBOT_TO_DATASET.get(patient_data["gender"], "Female")

    encoded = {
        "age":                  int(patient_data["age"]),
        "gender":               maps["gender"][gender_label],
        "fever":                maps["fever"][_yes_no(patient_data.get("has_fever", False))],
        "cough":                maps["cough"][_yes_no(patient_data.get("has_cough", False))],
        "fatigue":              maps["fatigue"][_yes_no(patient_data.get("has_fatigue", False))],
        "difficulty_breathing": maps["difficulty_breathing"][_yes_no(patient_data.get("has_difficulty_breathing", False))],
        "blood_pressure":       maps["blood_pressure"][_health_level(patient_data.get("blood_pressure", "Normal"))],
        "cholesterol_level":    maps["cholesterol_level"][_health_level(patient_data.get("cholesterol_level", "Normal"))],
    }

    return [encoded[col] for col in FEATURE_ORDER]
