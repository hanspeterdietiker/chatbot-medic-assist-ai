import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))

from chatbot.lifestyle_rules import (
    apply_lifestyle_reranking,
    escalate_for_lifestyle,
    lifestyle_factors,
)
from chatbot.urgency_triage_rules import (
    URGENCIA_BAIXA,
    URGENCIA_PRIORITARIO,
    URGENCIA_EMERGENCIA,
)


def _patient(smokes=False, drinks=False):
    return {"smokes": smokes, "drinks_alcohol": drinks}


# ---------------------------------------------------------------------------
# Re-ranqueamento do top-N
# ---------------------------------------------------------------------------

class TestRerank:
    def test_sem_habitos_nao_altera_ordem(self):
        probs = [("Common Cold", 0.5), ("Asthma", 0.3), ("Eczema", 0.2)]
        result = apply_lifestyle_reranking(probs, _patient())
        assert [d for d, _ in result] == ["Common Cold", "Asthma", "Eczema"]

    def test_fumante_eleva_doenca_respiratoria(self):
        # Asthma começa atrás mas deve subir com o boost do tabagismo
        probs = [("Eczema", 0.45), ("Asthma", 0.4), ("Acne", 0.15)]
        result = apply_lifestyle_reranking(probs, _patient(smokes=True))
        assert result[0][0] == "Asthma"

    def test_etilista_eleva_doenca_hepatica(self):
        probs = [("Common Cold", 0.5), ("Cirrhosis", 0.4), ("Acne", 0.1)]
        result = apply_lifestyle_reranking(probs, _patient(drinks=True))
        assert result[0][0] == "Cirrhosis"

    def test_probabilidades_renormalizadas(self):
        probs = [("Asthma", 0.4), ("Eczema", 0.6)]
        result = apply_lifestyle_reranking(probs, _patient(smokes=True))
        assert abs(sum(p for _, p in result) - 1.0) < 1e-9


# ---------------------------------------------------------------------------
# Escalada de urgência por hábito
# ---------------------------------------------------------------------------

class TestEscalada:
    def test_fumante_com_respiratoria_escala(self):
        out = escalate_for_lifestyle(URGENCIA_BAIXA, "Asthma", _patient(smokes=True))
        assert out == URGENCIA_PRIORITARIO

    def test_etilista_com_hepatica_escala(self):
        out = escalate_for_lifestyle(URGENCIA_PRIORITARIO, "Liver Disease", _patient(drinks=True))
        assert out == URGENCIA_EMERGENCIA

    def test_nao_escala_sem_associacao(self):
        out = escalate_for_lifestyle(URGENCIA_BAIXA, "Eczema", _patient(smokes=True))
        assert out == URGENCIA_BAIXA

    def test_escala_limitada_a_emergencia(self):
        out = escalate_for_lifestyle(URGENCIA_EMERGENCIA, "Asthma", _patient(smokes=True))
        assert out == URGENCIA_EMERGENCIA

    def test_sem_habitos_nao_escala(self):
        out = escalate_for_lifestyle(URGENCIA_BAIXA, "Asthma", _patient())
        assert out == URGENCIA_BAIXA


# ---------------------------------------------------------------------------
# Rótulos de fatores
# ---------------------------------------------------------------------------

class TestFatores:
    def test_lista_habitos_informados(self):
        assert lifestyle_factors(_patient(smokes=True, drinks=True)) == [
            "Tabagismo", "Consumo de álcool",
        ]

    def test_vazio_sem_habitos(self):
        assert lifestyle_factors(_patient()) == []
