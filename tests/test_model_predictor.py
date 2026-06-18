"""
Testes para integração chatbot ↔ modelo (B21) e encoder de paciente.

O modelo prevê doenças prováveis (top-N); área e urgência são derivadas da
doença #1. Hábitos (álcool/fumo) re-ranqueiam o top-N e escalam a urgência.
"""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))

try:
    import sklearn  # noqa: F401
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not SKLEARN_AVAILABLE,
    reason="scikit-learn não instalado",
)

ROOT_DIR      = pathlib.Path(__file__).parent.parent
MODELS_DIR    = ROOT_DIR / "models"
PROCESSED_DIR = ROOT_DIR / "dataset" / "processed"
TRAIN_CSV     = PROCESSED_DIR / "hospital-data-train.csv"


@pytest.fixture(scope="module")
def trained_models():
    """Garante que os modelos estejam treinados antes dos testes de predição."""
    if not TRAIN_CSV.exists():
        pytest.skip("Dataset de treino não encontrado — execute o pipeline de dados")

    if not (MODELS_DIR / "model_metadata.json").exists():
        from train_model import main as train_main
        train_main()

    # Reseta cache do predictor para recarregar modelos
    import chatbot.model_predictor as mp
    mp._models_cache = None
    mp._maps_cache = None
    mp._metadata_cache = None


def _base_patient(**overrides) -> dict:
    """Paciente simulado com valores padrão seguros (novo schema)."""
    data = {
        "age": 45,
        "gender": "Masculino",
        "selected_symptoms": ["Febre"],
        "has_fever": True,
        "has_cough": False,
        "has_fatigue": False,
        "has_difficulty_breathing": False,
        "has_intense_pain": False,
        "is_conscious": True,
        "blood_pressure": "Normal",
        "cholesterol_level": "Normal",
        "smokes": False,
        "drinks_alcohol": False,
        "symptom_duration_days": 2,
        "has_chronic_disease": False,
        "chronic_detail": "",
    }
    data.update(overrides)
    return data


class TestEmergenciaRegras:
    def test_inconsciencia_usa_regras_seguranca(self, trained_models):
        from chatbot.model_predictor import predict_triage
        from chatbot.recommended_area_rules import AREA_PRONTO_SOCORRO

        patient = _base_patient(is_conscious=False)
        diseases, area, urgency, source = predict_triage(patient)

        assert source == "regras_seguranca"
        assert area == AREA_PRONTO_SOCORRO
        assert urgency == "emergencia"
        assert diseases == []

    def test_dificuldade_respiratoria_usa_regras_seguranca(self, trained_models):
        from chatbot.model_predictor import predict_triage

        patient = _base_patient(has_difficulty_breathing=True)
        _, _, urgency, source = predict_triage(patient)

        assert source == "regras_seguranca"
        assert urgency == "emergencia"


class TestPredicaoModelo:
    def test_retorna_top_n_doencas(self, trained_models):
        from chatbot.model_predictor import predict_triage

        patient = _base_patient()
        diseases, area, urgency, source = predict_triage(patient)

        assert source.startswith("modelo_ia")
        assert 1 <= len(diseases) <= 5
        # cada item é (nome, probabilidade)
        for name, prob in diseases:
            assert isinstance(name, str)
            assert 0.0 <= prob <= 1.0
        # ordenado do mais provável ao menos provável
        probs = [p for _, p in diseases]
        assert probs == sorted(probs, reverse=True)
        assert area
        assert urgency in ("baixa", "prioritario", "emergencia")

    def test_dor_intensa_escala_urgencia(self, trained_models):
        from chatbot.model_predictor import predict_triage

        sem_dor = _base_patient(has_intense_pain=False)
        com_dor = _base_patient(has_intense_pain=True)
        _, _, urg_sem, _ = predict_triage(sem_dor)
        _, _, urg_com, _ = predict_triage(com_dor)

        order = {"baixa": 0, "prioritario": 1, "emergencia": 2}
        assert order[urg_com] >= order[urg_sem]

    def test_fumante_pode_alterar_ranking(self, trained_models):
        from chatbot.model_predictor import predict_triage

        # O re-ranqueamento por tabagismo não deve quebrar a predição
        patient = _base_patient(has_cough=True, smokes=True)
        diseases, _, _, source = predict_triage(patient)
        assert source.startswith("modelo_ia")
        assert len(diseases) >= 1


class TestFallback:
    def test_sem_modelos_usa_regras_fallback(self, monkeypatch):
        import chatbot.model_predictor as mp
        mp._models_cache = None
        mp._maps_cache = None
        mp._metadata_cache = None

        monkeypatch.setattr(mp, "_models_available", lambda: False)

        patient = _base_patient()
        diseases, area, urgency, source = mp.predict_triage(patient)

        assert source == "regras_fallback"
        assert diseases == []
        assert area
        assert urgency in ("baixa", "prioritario", "emergencia")


class TestPatientEncoder:
    def test_vetor_tem_oito_features(self, trained_models):
        from chatbot.patient_encoder import encode_patient_data, FEATURE_ORDER

        patient = _base_patient()
        vector = encode_patient_data(patient)

        assert len(vector) == len(FEATURE_ORDER) == 8
        assert all(isinstance(v, int) for v in vector)

    def test_genero_outro_usa_default(self, trained_models):
        from chatbot.patient_encoder import encode_patient_data

        patient = _base_patient(gender="Outro / Prefiro não informar")
        vector = encode_patient_data(patient)
        # índice 1 = gender, deve ser 0 (Female default) ou 1
        assert vector[1] in (0, 1)

    def test_proxies_saude_codificados(self, trained_models):
        from chatbot.patient_encoder import encode_patient_data

        patient = _base_patient(blood_pressure="Alta", cholesterol_level="Baixo")
        vector = encode_patient_data(patient)
        # blood_pressure (índice 6) e cholesterol (índice 7) viram inteiros 0/1/2
        assert vector[6] in (0, 1, 2)
        assert vector[7] in (0, 1, 2)
