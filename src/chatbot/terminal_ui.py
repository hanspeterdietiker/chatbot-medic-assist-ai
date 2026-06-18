"""
Interface visual do terminal para o Medic Assist AI (B26).

Usa a biblioteca `rich` para painéis coloridos, spinners de loading,
barra de progresso e badges de urgência — melhorando a experiência
sem depender de fundo preto ou texto ASCII plano.

Respeita a variável de ambiente NO_COLOR para acessibilidade.
"""

from __future__ import annotations

import os
from typing import Callable, TypeVar

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .messages import (
    AVISO_EMERGENCIA,
    AVISO_RESULTADO,
    ENCERRAMENTO,
    FONTE_MODELO_IA,
    FONTE_REGRAS_FALLBACK,
    FONTE_REGRAS_SEGURANCA,
    ORIENTACAO_URGENCIA,
)
from .translations import (
    translate_blood_pressure,
    translate_cholesterol,
    translate_disease,
)

T = TypeVar("T")

# Console compartilhado — force_terminal=False degrada bem em CI sem TTY
_console: Console | None = None


def get_console() -> Console:
    """Retorna o Console rich compartilhado (singleton)."""
    global _console
    if _console is None:
        no_color = os.environ.get("NO_COLOR", "") != ""
        _console = Console(force_terminal=not no_color, no_color=no_color)
    return _console


def reset_console(console: Console | None = None) -> None:
    """Redefine o console — útil em testes com StringIO."""
    global _console
    _console = console


def urgency_style(level: str) -> str:
    """
    Retorna estilo rich por nível de urgência.

    Verde=baixa, amarelo=prioritário, vermelho=emergência.
    """
    styles = {
        "baixa":       "bold green",
        "prioritario": "bold yellow",
        "emergencia":  "bold red",
    }
    return styles.get(level.lower(), "bold white")


def show_welcome() -> None:
    """Exibe painel de boas-vindas com avisos éticos."""
    console = get_console()
    body = (
        "Olá! Sou o [bold cyan]Medic Assist AI[/], assistente de apoio à "
        "triagem hospitalar inicial.\n\n"
        "[bold yellow]AVISO IMPORTANTE:[/]\n"
        "  • Este sistema [bold]NÃO[/] realiza diagnósticos médicos\n"
        "  • Este sistema [bold]NÃO[/] prescreve medicamentos\n"
        "  • Este sistema [bold]NÃO[/] substitui avaliação médica profissional\n"
        "  • As sugestões são apenas apoio ao encaminhamento inicial\n\n"
        "Em emergência com risco de vida: ligue [bold red]192 (SAMU)[/] "
        "ou vá ao pronto-socorro mais próximo."
    )
    console.print(Panel(
        body,
        title="[bold white]Medic Assist AI — Triagem Hospitalar[/]",
        border_style="cyan",
        padding=(1, 2),
    ))
    console.print()


def show_progress_bar(completed_steps: int, total: int) -> None:
    """
    Barra de progresso estática (sem live display).

    Usa renderização única para não bloquear console.input() durante as perguntas.
    O widget Progress do rich em modo live conflita com entrada interativa.
    """
    console = get_console()
    pct = int(completed_steps / total * 100) if total else 0
    filled = int(30 * completed_steps / total) if total else 0
    bar_fill = "[cyan]" + "━" * filled + "[/]"
    bar_empty = "[dim]" + "━" * (30 - filled) + "[/]"
    line = Text.from_markup(f"  Progresso: {bar_fill}{bar_empty}  ")
    line.append(f"{pct}% ", style="bold")
    line.append_text(Text.from_markup(f"[dim]({completed_steps}/{total} etapas)[/]"))
    console.print(line)
    console.print()


def show_step_header(step: int, total: int, title: str) -> None:
    """Cabeçalho colorido para cada etapa da conversa."""
    console = get_console()
    console.rule(
        f"[bold cyan]PASSO {step} de {total}[/] — {title}",
        style="cyan",
    )
    # Etapas já concluídas antes de iniciar esta (step 1 → 0 concluídas)
    show_progress_bar(step - 1, total)


def show_step_done(step: int, total: int, message: str) -> None:
    """Confirma conclusão de uma etapa e atualiza a barra de progresso."""
    console = get_console()
    console.print(f"  [bold green]✓[/] {message}")
    show_progress_bar(step, total)


def _print_error(message: str) -> None:
    """Exibe mensagem de erro estilizada."""
    get_console().print(f"  [bold red]✗[/]  {message}\n")


def prompt_text(
    prompt: str,
    validator: Callable[[str], bool] | None = None,
    error_msg: str = "Resposta inválida. Tente novamente.",
) -> str:
    """Solicita texto com validação e feedback visual de erro."""
    console = get_console()
    while True:
        answer = console.input(f"[bold cyan]?[/] {prompt}").strip()
        if validator is None or validator(answer):
            return answer
        _print_error(error_msg)


def prompt_choice(prompt: str, options: list[str]) -> tuple[int, str]:
    """Exibe opções numeradas e retorna (índice, texto escolhido)."""
    console = get_console()
    n = len(options)
    console.print(f"[bold]{prompt}[/]")
    for i, option in enumerate(options, 1):
        console.print(f"  [cyan]{i}.[/] {option}")
    while True:
        raw = console.input("[bold cyan]Sua escolha (número):[/] ").strip()
        if raw.isdigit() and 1 <= int(raw) <= n:
            index = int(raw) - 1
            return index, options[index]
        _print_error(f"Digite um número entre 1 e {n}.")


def prompt_multi_choice(
    prompt: str,
    options: list[str],
    max_select: int = 5,
) -> list[str]:
    """
    Exibe opções numeradas e permite selecionar várias (até max_select).

    Aceita números separados por vírgula/espaço (ex.: "1, 3 4").
    Enter sem nada = nenhuma opção selecionada.
    """
    console = get_console()
    n = len(options)
    console.print(f"[bold]{prompt}[/]")
    console.print(f"  [dim](selecione até {max_select} — números separados por vírgula, ou Enter para nenhum)[/]")
    for i, option in enumerate(options, 1):
        console.print(f"  [cyan]{i}.[/] {option}")
    while True:
        raw = console.input("[bold cyan]Suas escolhas:[/] ").strip()
        if raw == "":
            return []
        tokens = [t for t in raw.replace(",", " ").split() if t]
        if not all(t.isdigit() and 1 <= int(t) <= n for t in tokens):
            _print_error(f"Digite números entre 1 e {n}, separados por vírgula.")
            continue
        # Remove duplicatas preservando a ordem de seleção
        seen: list[int] = []
        for t in tokens:
            idx = int(t) - 1
            if idx not in seen:
                seen.append(idx)
        if len(seen) > max_select:
            _print_error(f"Selecione no máximo {max_select} opções.")
            continue
        return [options[i] for i in seen]


def prompt_yes_no(prompt: str) -> bool:
    """Pergunta sim/não com validação."""
    while True:
        raw = get_console().input(f"[bold cyan]?[/] {prompt} [dim](s/n)[/]: ").strip().lower()
        if raw in ("s", "sim", "y", "yes"):
            return True
        if raw in ("n", "nao", "não", "no"):
            return False
        _print_error("Responda com 's' para sim ou 'n' para não.")


def show_loading(message: str, task_fn: Callable[[], T]) -> T:
    """
    Executa task_fn com spinner animado (loading).

    Usado durante a predição do modelo de IA para feedback visual.
    """
    console = get_console()
    with console.status(f"[bold cyan]{message}[/]", spinner="dots"):
        return task_fn()


def _format_source_label(source: str) -> str:
    """Converte código interno da fonte em texto amigável."""
    if source.startswith("modelo_ia"):
        if "(" in source:
            algo = source.split("(")[1].rstrip(")")
            return f"{FONTE_MODELO_IA} ({algo})"
        return FONTE_MODELO_IA
    if source == "regras_seguranca":
        return FONTE_REGRAS_SEGURANCA
    return FONTE_REGRAS_FALLBACK


def _format_symptoms(patient_data: dict) -> str:
    """Resumo legível dos sintomas selecionados."""
    selected = patient_data.get("selected_symptoms")
    if selected:
        return ", ".join(selected)
    return "Nenhum sintoma selecionado"


def show_triage_result(
    patient_data: dict,
    diseases: list[tuple[str, float]],
    recommended_area: str,
    urgency_level: str,
    source: str = "regras_fallback",
) -> None:
    """Exibe resultado final em painéis e tabelas coloridas (B22 + B26)."""
    from .lifestyle_rules import lifestyle_factors

    console = get_console()
    urgency_key = urgency_level.lower()

    # Aviso ético
    console.print(Panel(
        AVISO_RESULTADO.strip(),
        border_style="yellow",
        padding=(0, 1),
    ))

    # Tabela com dados informados
    data_table = Table(show_header=False, box=None, padding=(0, 2))
    data_table.add_column("Campo", style="dim")
    data_table.add_column("Valor", style="white")
    data_table.add_row("Idade", f"{patient_data['age']} anos")
    data_table.add_row("Gênero", patient_data["gender"])
    data_table.add_row("Sintomas", _format_symptoms(patient_data))
    alert_signals = patient_data.get("selected_alert_signals")
    if alert_signals:
        data_table.add_row("Sinais de alerta", ", ".join(alert_signals))
    data_table.add_row("Pressão arterial", translate_blood_pressure(patient_data.get("blood_pressure", "Normal")))
    data_table.add_row("Colesterol", translate_cholesterol(patient_data.get("cholesterol_level", "Normal")))
    habitos = lifestyle_factors(patient_data)
    data_table.add_row("Hábitos", ", ".join(habitos) if habitos else "Nenhum informado")
    data_table.add_row("Duração sintomas", f"{patient_data.get('symptom_duration_days', 0)} dia(s)")
    if patient_data.get("has_chronic_disease"):
        data_table.add_row("Doença crônica", patient_data.get("chronic_detail", ""))

    console.print(Panel(
        data_table,
        title="[bold]Dados informados[/]",
        border_style="blue",
    ))

    # Tabela de doenças prováveis (top-N) com probabilidade
    if diseases:
        disease_table = Table(box=None, padding=(0, 2))
        disease_table.add_column("#", style="dim", justify="right")
        disease_table.add_column("Possível doença", style="white")
        disease_table.add_column("Probabilidade", style="cyan", justify="right")
        for i, (name, prob) in enumerate(diseases, 1):
            disease_table.add_row(str(i), translate_disease(name), f"{prob * 100:.1f}%")
        console.print(Panel(
            disease_table,
            title="[bold]Possíveis doenças (apoio — NÃO é diagnóstico)[/]",
            border_style="magenta",
        ))

    # Badge de urgência colorido
    urgency_text = Text(urgency_key.upper(), style=urgency_style(urgency_key))
    orientacao = ORIENTACAO_URGENCIA.get(urgency_key, "")

    rec_body = (
        f"[bold]Área sugerida:[/]     [cyan]{recommended_area}[/]\n"
        f"[bold]Nível de urgência:[/] {urgency_text}\n"
        f"[bold]Origem:[/]           [dim]{_format_source_label(source)}[/]"
    )
    if orientacao:
        rec_body += f"\n\n[bold yellow]O que fazer agora:[/]\n{orientacao}"

    border = "red" if urgency_key == "emergencia" else "green" if urgency_key == "baixa" else "yellow"
    console.print(Panel(
        rec_body,
        title="[bold]SUA TRIAGEM — Recomendação[/]",
        border_style=border,
        padding=(1, 2),
    ))

    if urgency_key == "emergencia":
        console.print(Panel(
            AVISO_EMERGENCIA.strip(),
            title="[bold red]EMERGÊNCIA[/]",
            border_style="red",
        ))

    console.print(Panel(
        ENCERRAMENTO.strip(),
        title="[bold]Triagem concluída[/]",
        border_style="cyan",
        padding=(0, 1),
    ))
