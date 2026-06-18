"""
Script de pré-processamento do dataset (B08 + B09).

Lê o CSV bruto (Disease Symptoms and Patient Profile Dataset), normaliza os
nomes de colunas para snake_case e anota cada registro com `area_recomendada`
e `nivel_urgencia` derivadas da doença (para EDA/relatório).

O alvo de Machine Learning é a coluna `disease`; área e urgência são derivadas
na inferência a partir da doença prevista (ver chatbot/model_predictor.py).

Uso:
    python src/preprocess_dataset.py
"""

import pathlib
import sys

try:
    import pandas as pd
except ImportError:
    print("pandas não encontrado. Execute: pip install pandas")
    sys.exit(1)

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from chatbot.recommended_area_rules import apply_area_rules
from chatbot.urgency_triage_rules import get_base_urgency, URGENCIA_EMERGENCIA

RAW_CSV = pathlib.Path(__file__).parent.parent / "dataset" / "raw" / "disease-symptoms-patient-profile.csv"
PROCESSED_DIR = pathlib.Path(__file__).parent.parent / "dataset" / "processed"
OUTPUT_CSV = PROCESSED_DIR / "hospital-data-labeled.csv"

# Mapeamento dos nomes originais (com espaços) para snake_case
COLUMN_RENAME = {
    "Disease":              "disease",
    "Fever":                "fever",
    "Cough":                "cough",
    "Fatigue":              "fatigue",
    "Difficulty Breathing": "difficulty_breathing",
    "Age":                  "age",
    "Gender":               "gender",
    "Blood Pressure":       "blood_pressure",
    "Cholesterol Level":    "cholesterol_level",
    "Outcome Variable":     "outcome",
}


def _label_row(row: pd.Series) -> pd.Series:
    """Deriva area_recomendada e nivel_urgencia a partir da doença e sintomas."""
    disease = str(row["disease"])
    age = int(row["age"])
    area = apply_area_rules(disease, age)

    urgency = get_base_urgency(disease)
    # Dificuldade respiratória é sinal de alerta — eleva para emergência
    if str(row["difficulty_breathing"]).strip().lower() in ("yes", "sim", "1", "true"):
        urgency = URGENCIA_EMERGENCIA

    return pd.Series({"area_recomendada": area, "nivel_urgencia": urgency})


def main() -> None:
    df = pd.read_csv(RAW_CSV)
    df = df.rename(columns=COLUMN_RENAME)

    df["disease"] = df["disease"].astype(str).str.strip()
    df["age"] = pd.to_numeric(df["age"], errors="coerce").fillna(0).astype(int)
    df.dropna(subset=["disease"], inplace=True)
    df = df[df["disease"] != ""]

    labels = df.apply(_label_row, axis=1)
    df = pd.concat([df, labels], axis=1)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)

    print(f"Dataset salvo em: {OUTPUT_CSV}")
    print(f"Total de registros: {len(df)} | Doenças distintas: {df['disease'].nunique()}\n")

    print("--- Distribuição por área recomendada ---")
    print(df["area_recomendada"].value_counts().to_string())

    print("\n--- Distribuição por nível de urgência ---")
    print(df["nivel_urgencia"].value_counts().to_string())


if __name__ == "__main__":
    main()
