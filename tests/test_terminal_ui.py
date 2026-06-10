"""
Testes para a interface visual do terminal (B26).
"""
import io
import pathlib
import re
import sys

_ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")


def _plain_output(text: str) -> str:
    """Remove códigos ANSI para validar conteúdo visível ao usuário."""
    return _ANSI_ESCAPE.sub("", text)

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))

try:
    from rich.console import Console
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

pytestmark = pytest.mark.skipif(not RICH_AVAILABLE, reason="rich não instalado")


@pytest.fixture(autouse=True)
def _reset_console():
    """Restaura console global após cada teste."""
    from chatbot.terminal_ui import reset_console
    yield
    reset_console()


@pytest.fixture
def capture_console():
    """Console rich redirecionado para StringIO."""
    from chatbot.terminal_ui import reset_console
    buffer = io.StringIO()
    console = Console(file=buffer, force_terminal=True, width=120)
    reset_console(console)
    return buffer, console


class TestUrgencyStyle:
    def test_baixa_verde(self):
        from chatbot.terminal_ui import urgency_style
        assert "green" in urgency_style("baixa")

    def test_prioritario_amarelo(self):
        from chatbot.terminal_ui import urgency_style
        assert "yellow" in urgency_style("prioritario")

    def test_emergencia_vermelho(self):
        from chatbot.terminal_ui import urgency_style
        assert "red" in urgency_style("emergencia")

    def test_desconhecido_fallback(self):
        from chatbot.terminal_ui import urgency_style
        assert urgency_style("outro") == "bold white"


class TestShowWelcome:
    def test_nao_lanca_excecao(self, capture_console):
        from chatbot.terminal_ui import show_welcome
        show_welcome()
        output = capture_console[0].getvalue()
        assert "Medic Assist AI" in output

    def test_contem_aviso_etico(self, capture_console):
        from chatbot.terminal_ui import show_welcome
        show_welcome()
        output = capture_console[0].getvalue()
        assert "NÃO" in output or "diagnóstico" in output.lower()


class TestShowTriageResult:
    def test_exibe_area_e_urgencia(self, capture_console):
        from chatbot.terminal_ui import show_triage_result

        patient = {
            "age": 45,
            "gender": "Masculino",
            "primary_condition": "Dor no Coração",
            "symptom_duration_days": 2,
            "has_chronic_disease": False,
            "chronic_detail": "",
        }
        show_triage_result(
            patient,
            "Cardiologia / Pronto-Socorro",
            "prioritario",
            "modelo_ia (Árvore de Decisão)",
        )
        output = capture_console[0].getvalue()
        assert "Cardiologia" in output
        assert "PRIORITARIO" in output or "prioritario" in output.lower()


class TestShowLoading:
    def test_executa_funcao_e_retorna_resultado(self, capture_console):
        from chatbot.terminal_ui import show_loading

        result = show_loading("Processando...", lambda: (1, 2, 3))
        assert result == (1, 2, 3)


class TestProgressBar:
    def test_barra_estatica_nao_lanca_excecao(self, capture_console):
        from chatbot.terminal_ui import show_progress_bar

        show_progress_bar(2, 4)
        output = _plain_output(capture_console[0].getvalue())
        assert "50%" in output
        assert "Progresso" in output


class TestPromptValidation:
    def test_prompt_text_aceita_valido(self, monkeypatch):
        from chatbot.terminal_ui import prompt_text

        monkeypatch.setattr(
            "chatbot.terminal_ui.get_console",
            lambda: type("C", (), {"input": lambda self, p: "25"})(),
        )
        assert prompt_text("Idade? ", validator=lambda x: x.isdigit()) == "25"
