"""
Traduções PT-BR para exibição ao paciente.

O modelo de IA e o dataset usam rótulos em inglês (ex.: "Ulcerative Colitis",
"High"). Estas tabelas convertem esses rótulos para português brasileiro na
camada de apresentação — sem alterar os dados internos usados pelas regras.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Doenças — rótulo do dataset (inglês) → nome em PT-BR.
# Inclui as variantes truncadas presentes no dataset (ex.: "Chronic
# Obstructive Pulmonary...") para que também sejam traduzidas corretamente.
# ---------------------------------------------------------------------------
DISEASE_PT: dict[str, str] = {
    "Acne": "Acne",
    "Allergic Rhinitis": "Rinite Alérgica",
    "Alzheimer's Disease": "Doença de Alzheimer",
    "Anemia": "Anemia",
    "Anxiety Disorders": "Transtornos de Ansiedade",
    "Appendicitis": "Apendicite",
    "Asthma": "Asma",
    "Atherosclerosis": "Aterosclerose",
    "Autism Spectrum Disorder (ASD)": "Transtorno do Espectro Autista (TEA)",
    "Bipolar Disorder": "Transtorno Bipolar",
    "Bladder Cancer": "Câncer de Bexiga",
    "Brain Tumor": "Tumor Cerebral",
    "Breast Cancer": "Câncer de Mama",
    "Bronchitis": "Bronquite",
    "Cataracts": "Catarata",
    "Cerebral Palsy": "Paralisia Cerebral",
    "Chickenpox": "Catapora",
    "Cholecystitis": "Colecistite",
    "Cholera": "Cólera",
    "Chronic Kidney Disease": "Doença Renal Crônica",
    "Chronic Obstructive Pulmonary Disease (COPD)": "Doença Pulmonar Obstrutiva Crônica (DPOC)",
    "Chronic Obstructive Pulmonary...": "Doença Pulmonar Obstrutiva Crônica (DPOC)",
    "Cirrhosis": "Cirrose",
    "Colorectal Cancer": "Câncer Colorretal",
    "Common Cold": "Resfriado Comum",
    "Conjunctivitis (Pink Eye)": "Conjuntivite",
    "Coronary Artery Disease": "Doença Arterial Coronariana",
    "Crohn's Disease": "Doença de Crohn",
    "Cystic Fibrosis": "Fibrose Cística",
    "Dementia": "Demência",
    "Dengue Fever": "Dengue",
    "Depression": "Depressão",
    "Diabetes": "Diabetes",
    "Diverticulitis": "Diverticulite",
    "Down Syndrome": "Síndrome de Down",
    "Eating Disorders (Anorexia,...": "Transtornos Alimentares (Anorexia, ...)",
    "Ebola Virus": "Vírus Ebola",
    "Eczema": "Eczema",
    "Endometriosis": "Endometriose",
    "Epilepsy": "Epilepsia",
    "Esophageal Cancer": "Câncer de Esôfago",
    "Fibromyalgia": "Fibromialgia",
    "Gastroenteritis": "Gastroenterite",
    "Glaucoma": "Glaucoma",
    "Gout": "Gota",
    "HIV/AIDS": "HIV/AIDS",
    "Hemophilia": "Hemofilia",
    "Hemorrhoids": "Hemorroidas",
    "Hepatitis": "Hepatite",
    "Hepatitis B": "Hepatite B",
    "Hyperglycemia": "Hiperglicemia",
    "Hypertension": "Hipertensão",
    "Hypertensive Heart Disease": "Doença Cardíaca Hipertensiva",
    "Hyperthyroidism": "Hipertireoidismo",
    "Hypoglycemia": "Hipoglicemia",
    "Hypothyroidism": "Hipotireoidismo",
    "Influenza": "Influenza (Gripe)",
    "Kidney Cancer": "Câncer de Rim",
    "Kidney Disease": "Doença Renal",
    "Klinefelter Syndrome": "Síndrome de Klinefelter",
    "Liver Cancer": "Câncer de Fígado",
    "Liver Disease": "Doença Hepática",
    "Lung Cancer": "Câncer de Pulmão",
    "Lyme Disease": "Doença de Lyme",
    "Lymphoma": "Linfoma",
    "Malaria": "Malária",
    "Marfan Syndrome": "Síndrome de Marfan",
    "Measles": "Sarampo",
    "Melanoma": "Melanoma",
    "Migraine": "Enxaqueca",
    "Multiple Sclerosis": "Esclerose Múltipla",
    "Mumps": "Caxumba",
    "Muscular Dystrophy": "Distrofia Muscular",
    "Myocardial Infarction (Heart...": "Infarto do Miocárdio (Ataque Cardíaco)",
    "Obsessive-Compulsive Disorde...": "Transtorno Obsessivo-Compulsivo (TOC)",
    "Osteoarthritis": "Osteoartrite",
    "Osteomyelitis": "Osteomielite",
    "Osteoporosis": "Osteoporose",
    "Otitis Media (Ear Infection)": "Otite Média (Infecção de Ouvido)",
    "Ovarian Cancer": "Câncer de Ovário",
    "Pancreatic Cancer": "Câncer de Pâncreas",
    "Pancreatitis": "Pancreatite",
    "Parkinson's Disease": "Doença de Parkinson",
    "Pneumocystis Pneumonia (PCP)": "Pneumonia por Pneumocystis (PCP)",
    "Pneumonia": "Pneumonia",
    "Pneumothorax": "Pneumotórax",
    "Polio": "Poliomielite",
    "Polycystic Ovary Syndrome (PCOS)": "Síndrome dos Ovários Policísticos (SOP)",
    "Prader-Willi Syndrome": "Síndrome de Prader-Willi",
    "Prostate Cancer": "Câncer de Próstata",
    "Psoriasis": "Psoríase",
    "Rabies": "Raiva",
    "Rheumatoid Arthritis": "Artrite Reumatoide",
    "Rubella": "Rubéola",
    "Schizophrenia": "Esquizofrenia",
    "Scoliosis": "Escoliose",
    "Sepsis": "Sepse",
    "Sickle Cell Anemia": "Anemia Falciforme",
    "Sinusitis": "Sinusite",
    "Sleep Apnea": "Apneia do Sono",
    "Spina Bifida": "Espinha Bífida",
    "Stroke": "AVC (Derrame)",
    "Systemic Lupus Erythematosus...": "Lúpus Eritematoso Sistêmico",
    "Testicular Cancer": "Câncer de Testículo",
    "Tetanus": "Tétano",
    "Thyroid Cancer": "Câncer de Tireoide",
    "Tonsillitis": "Amigdalite",
    "Tourette Syndrome": "Síndrome de Tourette",
    "Tuberculosis": "Tuberculose",
    "Turner Syndrome": "Síndrome de Turner",
    "Typhoid Fever": "Febre Tifoide",
    "Ulcerative Colitis": "Colite Ulcerativa",
    "Urinary Tract Infection": "Infecção do Trato Urinário (ITU)",
    "Urinary Tract Infection (UTI)": "Infecção do Trato Urinário (ITU)",
    "Williams Syndrome": "Síndrome de Williams",
    "Zika Virus": "Vírus Zika",
}

# ---------------------------------------------------------------------------
# Níveis de saúde (Low/Normal/High) → PT-BR.
# Colesterol usa gênero masculino (Baixo/Alto); pressão arterial usa
# feminino (Baixa/Alta).
# ---------------------------------------------------------------------------
CHOLESTEROL_PT: dict[str, str] = {"Low": "Baixo", "Normal": "Normal", "High": "Alto"}
BLOOD_PRESSURE_PT: dict[str, str] = {"Low": "Baixa", "Normal": "Normal", "High": "Alta"}


def translate_disease(name: str) -> str:
    """Traduz o nome da doença para PT-BR; mantém o original se não mapeado."""
    return DISEASE_PT.get(name, name)


def translate_cholesterol(level: str) -> str:
    """Traduz o nível de colesterol (Low/Normal/High) para PT-BR."""
    return CHOLESTEROL_PT.get(str(level), str(level))


def translate_blood_pressure(level: str) -> str:
    """Traduz o nível de pressão arterial (Low/Normal/High) para PT-BR."""
    return BLOOD_PRESSURE_PT.get(str(level), str(level))
