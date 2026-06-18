"""
Script de treinamento e avaliação dos modelos de classificação (B15–B20).

Treina Árvore de Decisão (B15) e Random Forest (B16) para prever a
**doença provável** (`disease`) a partir de sintomas e perfil de saúde.

Features disponíveis na triagem via chatbot:
  age, gender, fever, cough, fatigue, difficulty_breathing,
  blood_pressure, cholesterol_level

A área recomendada e o nível de urgência NÃO são alvos do modelo: são
derivados da doença prevista por regras clínicas (chatbot/model_predictor.py),
o que faz hábitos (álcool/fumo) refletirem de forma coerente nos três.

Como há muitas doenças (116) e poucas amostras por classe, reportamos
acurácia **top-1** e **top-5** — esta última é a métrica relevante para
sugerir "doenças prováveis".

Uso:
    python src/train_model.py
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
    import joblib
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, classification_report
except ImportError:
    print("scikit-learn não encontrado. Execute: pip install scikit-learn")
    sys.exit(1)

ROOT_DIR      = pathlib.Path(__file__).parent.parent
PROCESSED_DIR = ROOT_DIR / "dataset" / "processed"
MODELS_DIR    = ROOT_DIR / "models"
TRAIN_CSV     = PROCESSED_DIR / "hospital-data-train.csv"
TEST_CSV      = PROCESSED_DIR / "hospital-data-test.csv"
ENCODING_MAPS = PROCESSED_DIR / "encoding_maps.json"

# Features disponíveis na triagem — sintomas multi-seleção + perfil de saúde
FEATURE_COLS = [
    "age", "gender", "fever", "cough", "fatigue",
    "difficulty_breathing", "blood_pressure", "cholesterol_level",
]

# Alvo único: doença provável
TARGET_DISEASE = "disease"

# Quantas doenças prováveis o chatbot exibe (top-N)
TOP_K = 5

# Semente fixa para reprodutibilidade e comparação DT vs RF
RANDOM_STATE = 42

ALGO_DECISION_TREE = "decision_tree"
ALGO_RANDOM_FOREST = "random_forest"


def _load_splits() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carrega conjuntos de treino e teste gerados pelo split_dataset.py."""
    if not TRAIN_CSV.exists() or not TEST_CSV.exists():
        print("Conjuntos treino/teste não encontrados. Execute: python src/split_dataset.py")
        sys.exit(1)
    return pd.read_csv(TRAIN_CSV), pd.read_csv(TEST_CSV)


def _top_k_accuracy(model, X_test: pd.DataFrame, y_test: pd.Series, k: int) -> float:
    """
    Fração de exemplos cuja classe verdadeira está entre as k mais prováveis.

    Implementação manual (em vez de top_k_accuracy_score) para tolerar rótulos
    de teste ausentes do treino — comuns quando há muitas classes raras.
    """
    proba = model.predict_proba(X_test)
    classes = list(model.classes_)
    hits = 0
    for probs, true_label in zip(proba, y_test):
        top_idx = probs.argsort()[::-1][:k]
        top_labels = {classes[i] for i in top_idx}
        if true_label in top_labels:
            hits += 1
    return round(hits / len(y_test), 4) if len(y_test) else 0.0


def _evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """Calcula acurácia top-1, top-5 e classification_report (B17–B19)."""
    pred = model.predict(X_test)
    return {
        "accuracy": {
            "top1": round(float(accuracy_score(y_test, pred)), 4),
            f"top{TOP_K}": _top_k_accuracy(model, X_test, y_test, TOP_K),
        },
        "classification_report": classification_report(
            y_test, pred, output_dict=True, zero_division=0
        ),
    }


def _train_and_save(
    algo_name: str,
    model,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict:
    """Treina o modelo de doença, salva .joblib e retorna métricas."""
    model.fit(X_train, y_train)
    joblib.dump(model, MODELS_DIR / f"{algo_name}_disease.joblib")

    metrics = _evaluate_model(model, X_test, y_test)
    metrics["algorithm"] = algo_name

    with open(MODELS_DIR / f"metrics_{algo_name}.json", "w", encoding="utf-8") as fh:
        json.dump(metrics, fh, indent=2, ensure_ascii=False)

    return metrics


def main() -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    train_df, test_df = _load_splits()

    X_train = train_df[FEATURE_COLS]
    X_test  = test_df[FEATURE_COLS]
    y_train = train_df[TARGET_DISEASE]
    y_test  = test_df[TARGET_DISEASE]

    # B15 — Árvore de Decisão: interpretável, adequada para apresentação A3
    metrics_dt = _train_and_save(
        ALGO_DECISION_TREE,
        DecisionTreeClassifier(random_state=RANDOM_STATE),
        X_train, y_train, X_test, y_test,
    )

    # B16 — Random Forest: ensemble para comparação
    metrics_rf = _train_and_save(
        ALGO_RANDOM_FOREST,
        RandomForestClassifier(random_state=RANDOM_STATE, n_estimators=100),
        X_train, y_train, X_test, y_test,
    )

    # Seleciona algoritmo com maior acurácia top-5 (métrica de "doença provável")
    topk = f"top{TOP_K}"
    best = (
        ALGO_DECISION_TREE
        if metrics_dt["accuracy"][topk] >= metrics_rf["accuracy"][topk]
        else ALGO_RANDOM_FOREST
    )

    metadata = {
        "feature_columns": FEATURE_COLS,
        "target": TARGET_DISEASE,
        "top_k": TOP_K,
        "random_state": RANDOM_STATE,
        "best_algorithm": best,
        "comparison": {
            ALGO_DECISION_TREE: metrics_dt["accuracy"],
            ALGO_RANDOM_FOREST: metrics_rf["accuracy"],
        },
        "encoding_maps_file": str(ENCODING_MAPS.name),
    }

    with open(MODELS_DIR / "model_metadata.json", "w", encoding="utf-8") as fh:
        json.dump(metadata, fh, indent=2, ensure_ascii=False)

    print("Modelos treinados e salvos em:", MODELS_DIR)
    print(f"  Árvore de Decisão — top1: {metrics_dt['accuracy']['top1']} | {topk}: {metrics_dt['accuracy'][topk]}")
    print(f"  Random Forest     — top1: {metrics_rf['accuracy']['top1']} | {topk}: {metrics_rf['accuracy'][topk]}")
    print(f"  Algoritmo selecionado para o chatbot: {best}")


if __name__ == "__main__":
    main()
