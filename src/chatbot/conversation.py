from .terminal_ui import (
    show_step_header,
    show_step_done,
    show_triage_result,
    prompt_text,
    prompt_choice,
    prompt_yes_no,
    show_welcome,
)

CONDITIONS = [
    "Dor no Coração/Dor no Peito/ Heart Disease / Chest Pain",
    "AVC /Stroke / Neurological Issue",
    "Fratura/Fracture / Trauma",
    "Gripe / Dificuldade em Respirar / Flu / Respiratory Infection",
    "Complicacao na Gravidez/Pregnancy Complication",
    "Diabetes / High Glucose",
    "Doença de Pele/Skin Disease",
    "Other",
]

GENDERS = ["Masculino", "Feminino", "Outro / Prefiro não informar"]


def collect_patient_data() -> dict:
    """Executa a conversa guiada e retorna dados estruturados do paciente."""
    show_welcome()

    show_step_header(1, 4, "Dados básicos")
    age = int(prompt_text(
        "Qual é a sua idade? ",
        validator=lambda x: x.isdigit() and 0 < int(x) < 130,
        error_msg="Informe um número de idade válido (1–129).",
    ))
    _, gender = prompt_choice("Qual é o seu gênero?", GENDERS)
    show_step_done(1, 4, "Dados básicos concluídos")

    show_step_header(2, 4, "Condição principal")
    _, primary_condition = prompt_choice(
        "Qual melhor descreve o motivo da sua visita?", CONDITIONS
    )
    if primary_condition == "Other":
        primary_condition = prompt_text("Descreva brevemente sua condição: ")
    show_step_done(2, 4, "Condição registrada")

    show_step_header(3, 4, "Sintomas adicionais")
    has_fever = prompt_yes_no("Você está com febre?")
    has_intense_pain = prompt_yes_no("Você sente dor intensa?")
    has_difficulty_breathing = prompt_yes_no("Você tem dificuldade para respirar?")
    is_conscious = prompt_yes_no("Você está consciente e consegue responder sozinho?")
    show_step_done(3, 4, "Sintomas registrados")

    show_step_header(4, 4, "Histórico rápido")
    symptom_duration_days = int(prompt_text(
        "Há quantos dias você está com esses sintomas? ",
        validator=lambda x: x.isdigit() and int(x) >= 0,
        error_msg="Informe um número de dias válido (0 ou mais).",
    ))
    has_chronic_disease = prompt_yes_no("Você possui alguma doença crônica diagnosticada?")
    chronic_detail = (
        prompt_text("Qual(is) doença(s) crônica(s)? ")
        if has_chronic_disease else ""
    )
    show_step_done(4, 4, "Triagem concluída")

    return {
        "age": age,
        "gender": gender,
        "primary_condition": primary_condition,
        "has_fever": has_fever,
        "has_intense_pain": has_intense_pain,
        "has_difficulty_breathing": has_difficulty_breathing,
        "is_conscious": is_conscious,
        "symptom_duration_days": symptom_duration_days,
        "has_chronic_disease": has_chronic_disease,
        "chronic_detail": chronic_detail,
    }


def display_result(
    patient_data: dict,
    recommended_area: str,
    urgency_level: str,
    source: str = "regras_fallback",
) -> None:
    """Exibe resultado da triagem com interface visual aprimorada (B22 + B26)."""
    show_triage_result(patient_data, recommended_area, urgency_level, source)


def build_triage_summary(
    patient_data: dict,
    recommended_area: str,
    urgency_level: str,
    source: str = "regras_fallback",
) -> dict:
    """Retorna dict estruturado para revisão humana da triagem."""
    return {
        "patient": {
            "age": patient_data["age"],
            "gender": patient_data["gender"],
            "primary_condition": patient_data["primary_condition"],
            "symptom_duration_days": patient_data["symptom_duration_days"],
            "has_fever": patient_data["has_fever"],
            "has_intense_pain": patient_data["has_intense_pain"],
            "has_difficulty_breathing": patient_data["has_difficulty_breathing"],
            "is_conscious": patient_data["is_conscious"],
            "has_chronic_disease": patient_data["has_chronic_disease"],
            "chronic_detail": patient_data["chronic_detail"],
        },
        "recommendation": {
            "area_recomendada": recommended_area,
            "nivel_urgencia": urgency_level,
        },
        "prediction_source": source,
        "disclaimer": (
            "Triagem gerada automaticamente pelo Medic Assist AI. "
            "Não representa diagnóstico. Validação clínica obrigatória."
        ),
    }
