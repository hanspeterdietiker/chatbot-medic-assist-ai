"""
Script de pré-processamento do dataset (B08 + B09).

Lê o CSV bruto, aplica as regras de área e urgência e salva o dataset
anotado com as colunas `area_recomendada` e `nivel_urgencia`.

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
from chatbot.urgency_triage_rules import get_base_urgency

RAW_CSV = pathlib.Path(__file__).parent.parent / "dataset" / "raw" / "hospital-data-analysis.csv"
PROCESSED_DIR = pathlib.Path(__file__).parent.parent / "dataset" / "processed"
OUTPUT_CSV = PROCESSED_DIR / "hospital-data-labeled.csv"


def _label_row(row: pd.Series) -> pd.Series:
    condition = str(row["Condition"])
    age = int(row["Age"])
    area    = apply_area_rules(condition, age)
    urgency = get_base_urgency(condition)
    return pd.Series({"area_recomendada": area, "nivel_urgencia": urgency})


def main() -> None:
    df = pd.read_csv(RAW_CSV, sep=";")

    df["Condition"] = df["Condition"].astype(str).str.strip()
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce").fillna(0).astype(int)
    df.dropna(subset=["Condition"], inplace=True)
    df = df[df["Condition"] != ""]

    labels = df.apply(_label_row, axis=1)
    df = pd.concat([df, labels], axis=1)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)

    print(f"Dataset salvo em: {OUTPUT_CSV}")
    print(f"Total de registros: {len(df)}\n")

    print("--- Distribuição por área recomendada ---")
    print(df["area_recomendada"].value_counts().to_string())

    print("\n--- Distribuição por nível de urgência ---")
    print(df["nivel_urgencia"].value_counts().to_string())


if __name__ == "__main__":
    main()
