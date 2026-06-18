"""
Testes para o script de treinamento e avaliação (B15–B20).

O fixture `trained_models` executa train_model.main() uma vez por sessão.
O modelo prevê a doença provável (`disease`); métricas são top-1 e top-5.
"""
import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    import sklearn  # noqa: F401
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not (PANDAS_AVAILABLE and SKLEARN_AVAILABLE),
    reason="pandas e/ou scikit-learn não instalados",
)

ROOT_DIR      = pathlib.Path(__file__).parent.parent
MODELS_DIR    = ROOT_DIR / "models"
PROCESSED_DIR = ROOT_DIR / "dataset" / "processed"
TRAIN_CSV     = PROCESSED_DIR / "hospital-data-train.csv"
TEST_CSV      = PROCESSED_DIR / "hospital-data-test.csv"

ALGORITHMS = ["decision_tree", "random_forest"]
EXPECTED_FEATURES = [
    "age", "gender", "fever", "cough", "fatigue",
    "difficulty_breathing", "blood_pressure", "cholesterol_level",
]


@pytest.fixture(scope="module")
def trained_models():
    """Executa train_model.main() uma vez e retorna metadados."""
    if not TRAIN_CSV.exists() or not TEST_CSV.exists():
        pytest.skip("Conjuntos treino/teste não encontrados — execute src/split_dataset.py")

    from train_model import main, TOP_K
    main()

    with open(MODELS_DIR / "model_metadata.json", encoding="utf-8") as fh:
        metadata = json.load(fh)
    metadata["_top_k"] = TOP_K
    return metadata


class TestArtefatosModelo:
    def test_modelos_disease_joblib_criados(self, trained_models):
        for algo in ALGORITHMS:
            assert (MODELS_DIR / f"{algo}_disease.joblib").exists()

    def test_metricas_json_criados(self, trained_models):
        for algo in ALGORITHMS:
            assert (MODELS_DIR / f"metrics_{algo}.json").exists()

    def test_model_metadata_criado(self, trained_models):
        assert (MODELS_DIR / "model_metadata.json").exists()


class TestMetricas:
    @pytest.mark.parametrize("algo", ALGORITHMS)
    def test_acuracia_top1_e_topk_entre_zero_e_um(self, trained_models, algo):
        topk = f"top{trained_models['_top_k']}"
        with open(MODELS_DIR / f"metrics_{algo}.json", encoding="utf-8") as fh:
            metrics = json.load(fh)
        for chave in ("top1", topk):
            acc = metrics["accuracy"][chave]
            assert 0.0 <= acc <= 1.0

    @pytest.mark.parametrize("algo", ALGORITHMS)
    def test_topk_maior_ou_igual_top1(self, trained_models, algo):
        topk = f"top{trained_models['_top_k']}"
        with open(MODELS_DIR / f"metrics_{algo}.json", encoding="utf-8") as fh:
            metrics = json.load(fh)
        assert metrics["accuracy"][topk] >= metrics["accuracy"]["top1"]

    @pytest.mark.parametrize("algo", ALGORITHMS)
    def test_classification_report_presente(self, trained_models, algo):
        with open(MODELS_DIR / f"metrics_{algo}.json", encoding="utf-8") as fh:
            metrics = json.load(fh)
        assert "accuracy" in metrics["classification_report"]


class TestSelecaoAlgoritmo:
    def test_best_algorithm_valido(self, trained_models):
        assert trained_models["best_algorithm"] in ALGORITHMS

    def test_target_disease(self, trained_models):
        assert trained_models["target"] == "disease"

    def test_feature_columns_corretas(self, trained_models):
        assert trained_models["feature_columns"] == EXPECTED_FEATURES
