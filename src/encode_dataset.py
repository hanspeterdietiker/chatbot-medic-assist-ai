"""
Script de codificação de variáveis categóricas (B10).

Lê o dataset anotado (hospital-data-labeled.csv), converte todas as
colunas categóricas para valores numéricos e salva:
  - hospital-data-encoded.csv  — dataset pronto para modelos de ML
  - encoding_maps.json         — mapeamentos para rastreabilidade e auditoria

Os mapeamentos são obrigatórios em sistemas de saúde: permitem converter
qualquer previsão numérica do modelo de volta ao rótulo humano original
(em especial a coluna `disease`, alvo do modelo), garantindo transparência
e responsabilização ética.

Uso:
    python src/encode_dataset.py
"""

import json
import pathlib
import sys

try:
    import pandas as pd
except ImportError:
    print("pandas não encontrado. Execute: pip install pandas")
    sys.exit(1)

try:
    from sklearn.preprocessing import LabelEncoder
except ImportError:
    print("scikit-learn não encontrado. Execute: pip install scikit-learn")
    sys.exit(1)

PROCESSED_DIR = pathlib.Path(__file__).parent.parent / "dataset" / "processed"
INPUT_CSV     = PROCESSED_DIR / "hospital-data-labeled.csv"
OUTPUT_CSV    = PROCESSED_DIR / "hospital-data-encoded.csv"
MAPS_JSON     = PROCESSED_DIR / "encoding_maps.json"

# Mapa determinístico para colunas binárias — valores fixos independentes da
# ordem em que aparecem no dataset, garantindo reprodutibilidade entre execuções.
BINARY_MAPS: dict[str, dict[str, int]] = {
    "gender":               {"Female": 0, "Male": 1},
    "fever":                {"No": 0, "Yes": 1},
    "cough":                {"No": 0, "Yes": 1},
    "fatigue":              {"No": 0, "Yes": 1},
    "difficulty_breathing": {"No": 0, "Yes": 1},
    "outcome":              {"Negative": 0, "Positive": 1},
}

# Codificação ordinal preserva a ordem semântica clínica:
#   baixa (0) < prioritario (1) < emergencia (2)
URGENCY_ORDINAL: dict[str, int] = {
    "baixa":       0,
    "prioritario": 1,
    "emergencia":  2,
}

# Proxies de saúde — ordem clínica natural: Low (0) < Normal (1) < High (2).
# Usados como features do modelo (substituem hábitos como álcool/fumo).
HEALTH_ORDINAL: dict[str, int] = {
    "Low":    0,
    "Normal": 1,
    "High":   2,
}
HEALTH_ORDINAL_COLS: list[str] = ["blood_pressure", "cholesterol_level"]

# Colunas nominais sem ordem natural — codificadas com LabelEncoder.
# `disease` é o alvo do modelo; `area_recomendada` é mantida para EDA/relatório.
LABEL_ENCODE_COLS: list[str] = ["disease", "area_recomendada"]


def _apply_binary_maps(df: pd.DataFrame, maps: dict) -> dict:
    """Aplica mapas binários ao DataFrame e retorna os mapeamentos para o JSON."""
    saved: dict = {}
    for col, mapping in maps.items():
        df[col] = df[col].map(mapping)
        saved[col] = mapping
    return saved


def _apply_health_ordinal(df: pd.DataFrame) -> dict:
    """Aplica codificação ordinal Low<Normal<High a pressão e colesterol."""
    saved: dict = {}
    for col in HEALTH_ORDINAL_COLS:
        df[col] = df[col].map(HEALTH_ORDINAL)
        saved[col] = HEALTH_ORDINAL
    return saved


def _apply_label_encoders(df: pd.DataFrame, columns: list) -> dict:
    """
    Aplica LabelEncoder a colunas nominais.

    Retorna um dict {coluna: {rótulo_original: inteiro}} para que os
    resultados do modelo possam ser convertidos de volta ao texto original.
    """
    saved: dict = {}
    for col in columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        saved[col] = {label: int(i) for i, label in enumerate(le.classes_)}
    return saved


def _apply_ordinal(df: pd.DataFrame) -> dict:
    """Aplica codificação ordinal à coluna nivel_urgencia (baixa<prioritario<emergencia)."""
    df["nivel_urgencia"] = df["nivel_urgencia"].map(URGENCY_ORDINAL)
    return {"nivel_urgencia": URGENCY_ORDINAL}


def main() -> None:
    df = pd.read_csv(INPUT_CSV)

    all_maps: dict = {}

    # 1. Binárias (gender, sintomas, outcome) — mapas fixos e documentados
    all_maps.update(_apply_binary_maps(df, BINARY_MAPS))

    # 2. Ordinais de saúde (pressão, colesterol) — Low<Normal<High
    all_maps.update(_apply_health_ordinal(df))

    # 3. Ordinal (nivel_urgencia) — preserva hierarquia clínica
    all_maps.update(_apply_ordinal(df))

    # 4. Nominais (disease, area_recomendada) — LabelEncoder
    all_maps.update(_apply_label_encoders(df, LABEL_ENCODE_COLS))

    df.to_csv(OUTPUT_CSV, index=False)

    # Salva mapeamentos em JSON legível por humanos — requisito ético do projeto
    with open(MAPS_JSON, "w", encoding="utf-8") as fh:
        json.dump(all_maps, fh, indent=2, ensure_ascii=False)

    print(f"Dataset codificado salvo em: {OUTPUT_CSV}")
    print(f"Mapeamentos salvos em:       {MAPS_JSON}")
    print(f"Total de registros: {len(df)}")
    print(f"Colunas: {list(df.columns)}")


if __name__ == "__main__":
    main()
