from .terminal_ui import (
    show_step_header,
    show_step_done,
    show_triage_result,
    prompt_text,
    prompt_choice,
    prompt_multi_choice,
    prompt_yes_no,
    show_welcome,
)

# Sintomas oferecidos na multi-seleção. As 4 primeiras são features do modelo;
# "Dor intensa" alimenta as regras clínicas (não é coluna do dataset).
SYMPTOM_OPTIONS = [
    "Febre",
    "Tosse",
    "Fadiga / cansaço",
    "Dificuldade para respirar",
    "Dor intensa / dor no peito",
]

# Mapa rótulo de sintoma → chave booleana em patient_data
SYMPTOM_TO_FLAG = {
    "Febre":                       "has_fever",
    "Tosse":                       "has_cough",
    "Fadiga / cansaço":            "has_fatigue",
    "Dificuldade para respirar":   "has_difficulty_breathing",
    "Dor intensa / dor no peito":  "has_intense_pain",
}

# Sinais de alerta (passo 3) — mescla de sinais 🔴 (emergência) e 🟡 (urgência).
# Ordem: críticos primeiro para dar destaque visual à gravidade.
ALERT_SIGNAL_OPTIONS = [
    "Sangramento intenso",
    "Convulsão",
    "Confusão mental súbita",
    "Dormência ou fraqueza em um lado do corpo",
    "Vômito persistente",
    "Dor abdominal forte",
    "Tontura",
    "Palpitações",
]

# Mapa rótulo de sinal → chave booleana. As flags casam com
# EMERGENCY_SIGNAL_FLAGS / URGENCY_SIGNAL_FLAGS em urgency_triage_rules.py.
ALERT_SIGNAL_TO_FLAG = {
    "Sangramento intenso":                        "has_severe_bleeding",
    "Convulsão":                                  "has_seizure",
    "Confusão mental súbita":                     "has_sudden_confusion",
    "Dormência ou fraqueza em um lado do corpo":  "has_unilateral_weakness",
    "Vômito persistente":                         "has_persistent_vomiting",
    "Dor abdominal forte":                        "has_severe_abdominal_pain",
    "Tontura":                                    "has_dizziness",
    "Palpitações":                                "has_palpitations",
}

GENDERS = ["Masculino", "Feminino", "Outro / Prefiro não informar"]

# Opções de perfil de saúde (proxies) → rótulo canônico Low/Normal/High
BLOOD_PRESSURE_OPTIONS = ["Baixa", "Normal", "Alta", "Não sei"]
CHOLESTEROL_OPTIONS = ["Baixo", "Normal", "Alto", "Não sei"]
_HEALTH_CANONICAL = {
    "Baixa": "Low", "Baixo": "Low",
    "Normal": "Normal",
    "Alta": "High", "Alto": "High",
    "Não sei": "Normal",
}

# Hábitos (multi-seleção) → chaves booleanas
HABIT_OPTIONS = ["Fumo / tabagismo", "Consumo de álcool"]
HABIT_TO_FLAG = {
    "Fumo / tabagismo": "smokes",
    "Consumo de álcool": "drinks_alcohol",
}

TOTAL_STEPS = 6


def collect_patient_data() -> dict:
    """Executa a conversa guiada e retorna dados estruturados do paciente."""
    show_welcome()

    # Passo 1 — dados básicos
    show_step_header(1, TOTAL_STEPS, "Dados básicos")
    age = int(prompt_text(
        "Qual é a sua idade? ",
        validator=lambda x: x.isdigit() and 0 < int(x) < 130,
        error_msg="Informe um número de idade válido (1–129).",
    ))
    _, gender = prompt_choice("Qual é o seu gênero?", GENDERS)
    show_step_done(1, TOTAL_STEPS, "Dados básicos concluídos")

    # Passo 2 — sintomas (multi-seleção, até 5)
    show_step_header(2, TOTAL_STEPS, "Sintomas")
    selected_symptoms = prompt_multi_choice(
        "Quais sintomas você apresenta?", SYMPTOM_OPTIONS, max_select=5
    )
    symptom_flags = {flag: False for flag in SYMPTOM_TO_FLAG.values()}
    for symptom in selected_symptoms:
        symptom_flags[SYMPTOM_TO_FLAG[symptom]] = True
    is_conscious = prompt_yes_no("Você está consciente e consegue responder sozinho?")
    show_step_done(2, TOTAL_STEPS, "Sintomas registrados")

    # Passo 3 — sinais de alerta (mescla emergência 🔴 / urgência 🟡)
    show_step_header(3, TOTAL_STEPS, "Sinais de alerta")
    selected_alert_signals = prompt_multi_choice(
        "Você apresenta algum destes sinais de alerta?",
        ALERT_SIGNAL_OPTIONS,
        max_select=len(ALERT_SIGNAL_OPTIONS),
        none_option="Não tenho nenhum destes sinais de alerta",
    )
    alert_signal_flags = {flag: False for flag in ALERT_SIGNAL_TO_FLAG.values()}
    for signal in selected_alert_signals:
        alert_signal_flags[ALERT_SIGNAL_TO_FLAG[signal]] = True
    show_step_done(3, TOTAL_STEPS, "Sinais de alerta registrados")

    # Passo 4 — perfil de saúde (proxies: pressão e colesterol)
    show_step_header(4, TOTAL_STEPS, "Perfil de saúde")
    _, bp_label = prompt_choice("Como está sua pressão arterial?", BLOOD_PRESSURE_OPTIONS)
    _, chol_label = prompt_choice("Como está seu colesterol?", CHOLESTEROL_OPTIONS)
    show_step_done(4, TOTAL_STEPS, "Perfil de saúde registrado")

    # Passo 5 — hábitos de vida (multi-seleção)
    show_step_header(5, TOTAL_STEPS, "Hábitos de vida")
    selected_habits = prompt_multi_choice(
        "Você tem algum destes hábitos?",
        HABIT_OPTIONS,
        max_select=2,
        none_option="Não tenho nenhum destes hábitos",
    )
    habit_flags = {flag: False for flag in HABIT_TO_FLAG.values()}
    for habit in selected_habits:
        habit_flags[HABIT_TO_FLAG[habit]] = True
    show_step_done(5, TOTAL_STEPS, "Hábitos registrados")

    # Passo 6 — histórico rápido
    show_step_header(6, TOTAL_STEPS, "Histórico rápido")
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
    show_step_done(6, TOTAL_STEPS, "Triagem concluída")

    return {
        "age": age,
        "gender": gender,
        "selected_symptoms": selected_symptoms,
        **symptom_flags,
        "selected_alert_signals": selected_alert_signals,
        **alert_signal_flags,
        "is_conscious": is_conscious,
        "blood_pressure": _HEALTH_CANONICAL.get(bp_label, "Normal"),
        "cholesterol_level": _HEALTH_CANONICAL.get(chol_label, "Normal"),
        **habit_flags,
        "symptom_duration_days": symptom_duration_days,
        "has_chronic_disease": has_chronic_disease,
        "chronic_detail": chronic_detail,
    }


def display_result(
    patient_data: dict,
    diseases: list[tuple[str, float]],
    recommended_area: str,
    urgency_level: str,
    source: str = "regras_fallback",
) -> None:
    """Exibe resultado da triagem com interface visual aprimorada (B22 + B26)."""
    show_triage_result(patient_data, diseases, recommended_area, urgency_level, source)


def build_triage_summary(
    patient_data: dict,
    diseases: list[tuple[str, float]],
    recommended_area: str,
    urgency_level: str,
    source: str = "regras_fallback",
) -> dict:
    """Retorna dict estruturado para revisão humana da triagem."""
    return {
        "patient": {
            "age": patient_data["age"],
            "gender": patient_data["gender"],
            "selected_symptoms": patient_data.get("selected_symptoms", []),
            "selected_alert_signals": patient_data.get("selected_alert_signals", []),
            "blood_pressure": patient_data.get("blood_pressure", "Normal"),
            "cholesterol_level": patient_data.get("cholesterol_level", "Normal"),
            "smokes": patient_data.get("smokes", False),
            "drinks_alcohol": patient_data.get("drinks_alcohol", False),
            "symptom_duration_days": patient_data.get("symptom_duration_days", 0),
            "is_conscious": patient_data.get("is_conscious", True),
            "has_chronic_disease": patient_data.get("has_chronic_disease", False),
            "chronic_detail": patient_data.get("chronic_detail", ""),
        },
        "recommendation": {
            "possible_diseases": [
                {"disease": name, "probability": round(prob, 4)}
                for name, prob in diseases
            ],
            "area_recomendada": recommended_area,
            "nivel_urgencia": urgency_level,
        },
        "prediction_source": source,
        "disclaimer": (
            "Triagem gerada automaticamente pelo Medic Assist AI. "
            "As doenças listadas são possibilidades de apoio, NÃO um diagnóstico. "
            "Validação clínica obrigatória."
        ),
    }
