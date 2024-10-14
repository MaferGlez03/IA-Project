from Simulation.Hospital import Utility,Procedure
utilities = {
    "Syringe": Utility("Syringe", 100),
    "Stethoscope": Utility("Stethoscope", 50),
    "ECG Machine": Utility("ECG Machine", 10),
    "X-Ray Machine": Utility("X-Ray Machine", 5),
    "MRI Machine": Utility("MRI Machine", 3),
    "Blood Test Kit": Utility("Blood Test Kit", 200),
    "Thermometer": Utility("Thermometer", 80),
    "Blood Pressure Monitor": Utility("Blood Pressure Monitor", 70),
    "Ultrasound Machine": Utility("Ultrasound Machine", 6),
    "Defibrillator": Utility("Defibrillator", 10),
    "IV Drip": Utility("IV Drip", 150),
    "Ventilator": Utility("Ventilator", 15),
    "Oxygen Tank": Utility("Oxygen Tank", 50),
    "CT Scanner": Utility("CT Scanner", 2),
    "Heart Rate Monitor": Utility("Heart Rate Monitor", 30),
}

# Crear procedimientos para diagnosticar síntomas
diagnosis_procedures = [
    Procedure("Blood Test", [utilities["Blood Test Kit"]], "Analyze blood for anomalies", {"fever", "fatigue"}, "diagnosis"),
    Procedure("ECG", [utilities["ECG Machine"]], "Monitor heart activity", {"chest pain", "irregular heartbeat"}, "diagnosis"),
    Procedure("X-Ray", [utilities["X-Ray Machine"]], "Visualize bones and organs", {"shortness of breath", "lung infection"}, "diagnosis"),
    Procedure("MRI Scan", [utilities["MRI Machine"]], "Detailed imaging of soft tissues", {"tumor", "inflammation"}, "diagnosis"),
    Procedure("Ultrasound", [utilities["Ultrasound Machine"]], "Visualize internal organs", {"abdominal pain", "swelling"}, "diagnosis"),
    Procedure("Physical Exam", [utilities["Stethoscope"], utilities["Thermometer"]], "General body checkup", {"fever", "cough", "fatigue"}, "diagnosis"),
    Procedure("Blood Pressure Test", [utilities["Blood Pressure Monitor"]], "Measure blood pressure", {"high blood pressure", "dizziness"}, "diagnosis"),
    Procedure("CT Scan", [utilities["CT Scanner"]], "3D imaging of internal structures", {"internal bleeding", "tumor"}, "diagnosis"),
    Procedure("Pulmonary Function Test", [utilities["Ventilator"]], "Assess lung function", {"shortness of breath", "asthma"}, "diagnosis"),
    Procedure("Colonoscopy", [utilities["Syringe"], utilities["Ultrasound Machine"]], "Examine the colon", {"abdominal pain", "rectal bleeding"}, "diagnosis")
]

# Crear procedimientos para tratar síntomas
# treatment_procedures = [
#     Procedure("Defibrillation", [utilities["Defibrillator"]], "Correct heart arrhythmia", "good", "treatment"),
#     Procedure("IV Therapy", [utilities["IV Drip"]], "Administer fluids or medication", "normal", "treatment"),
#     Procedure("Oxygen Therapy", [utilities["Oxygen Tank"]], "Provide supplemental oxygen", "good", "treatment"),
#     Procedure("Ventilation", [utilities["Ventilator"]], "Assist with breathing", "normal", "treatment"),
#     Procedure("Heart Rate Monitoring", [utilities["Heart Rate Monitor"]], "Monitor heart rate continuously", "normal", "treatment"),
#     Procedure("Vaccination", [utilities["Syringe"]], "Administer vaccine", "good", "treatment"),
#     Procedure("Wound Dressing", [utilities["Syringe"]], "Clean and dress wound", "good", "treatment"),
#     Procedure("Biopsy", [utilities["Syringe"], utilities["Blood Test Kit"]], "Take tissue sample for analysis", "normal", "treatment"),
#     Procedure("Intravenous Injection", [utilities["Syringe"], utilities["IV Drip"]], "Inject medication into the bloodstream", "good", "treatment"),
#     Procedure("Dialysis", [utilities["IV Drip"]], "Remove waste from the blood", "good", "treatment"),
#     Procedure("Oxygen Saturation Test", [utilities["Oxygen Tank"]], "Check oxygen levels in blood", "normal", "treatment"),
# ]

treatment_procedures = [
    Procedure("Cognitive Therapy", [utilities["Stethoscope"]], "Improve cognitive function", "normal", "diagnosis"),
    Procedure("Cholinesterase Inhibitors", [utilities["Syringe"], utilities["IV Drip"]], "Slow progression of Alzheimer's", "good", "treatment"),
    Procedure("Medications to Manage Symptoms", [utilities["Syringe"], utilities["IV Drip"]], "Alleviate symptoms of disease", "normal", "treatment"),
    Procedure("Medications like Beta-Blockers", [utilities["Syringe"]], "Control heart rate", "normal", "treatment"),
    Procedure("Surgery for Severe Cases", [utilities["Syringe"], utilities["IV Drip"], utilities["Ventilator"]], "Correct structural issues", "good", "treatment"),
    Procedure("Speech Therapy", [utilities["Stethoscope"]], "Improve communication", "normal", "treatment"),
    Procedure("Augmentative Communication Devices", [], "Assist with communication", "good", "diagnosis"),
    Procedure("Cognitive Behavioral Therapy", [utilities["Stethoscope"]], "Treat mental health conditions", "good", "diagnosis"),
    Procedure("Medications", [utilities["Syringe"], utilities["IV Drip"]], "General symptom management", "normal", "treatment"),
    Procedure("Antipsychotic Medications", [utilities["Syringe"]], "Manage psychosis", "normal", "treatment"),
    Procedure("Supportive Therapy", [], "Provide emotional support", "good", "treatment"),
    Procedure("Cognitive Therapies", [utilities["Stethoscope"]], "Improve cognitive function", "normal", "diagnosis"),
    Procedure("Medications to Slow Progression", [utilities["Syringe"], utilities["IV Drip"]], "Slow down disease progression", "good", "treatment"),
    Procedure("Assistive Devices like Walkers", [], "Help with mobility", "good", "diagnosis"),
    Procedure("Pain Management Therapies", [utilities["Syringe"], utilities["Blood Test Kit"]], "Manage chronic pain", "normal", "diagnosis"),
    Procedure("Medications for Nerve Pain", [utilities["Syringe"], utilities["IV Drip"]], "Alleviate nerve pain", "normal", "treatment"),
    Procedure("Levodopa Medication", [utilities["Syringe"]], "Treat Parkinson's symptoms", "good", "treatment"),
    Procedure("Physical Therapy", [utilities["Stethoscope"]], "Improve mobility and strength", "good", "treatment"),
    Procedure("Psychotherapy", [utilities["Stethoscope"]], "Treat mental health conditions", "good", "treatment"),
    Procedure("Medications such as Antidepressants", [utilities["Syringe"], utilities["IV Drip"]], "Treat depression", "good", "treatment"),
    Procedure("Antiepileptic Medications", [utilities["Syringe"]], "Control seizures", "good", "treatment"),
    Procedure("Surgery in Refractory Cases", [utilities["Syringe"], utilities["IV Drip"], utilities["Ventilator"]], "Treat epilepsy in severe cases", "good", "treatment"),
    Procedure("Medications for Heart Health", [utilities["Syringe"], utilities["IV Drip"]], "Improve heart function", "good", "treatment"),
    Procedure("Lifestyle Changes", [], "Improve overall health", "normal", "diagnosis")
]

def create_procedures():
    procedures=[]
    procedures.extend(treatment_procedures)
    procedures.extend(diagnosis_procedures)
    return procedures


