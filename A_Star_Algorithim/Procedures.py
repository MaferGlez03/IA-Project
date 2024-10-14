from A_Star_Algorithim.Support import Procedure, Medication
treatment_procedures = [
    Procedure(
        name="Cognitive Therapy",
        cost=300,
        effects_progress=5,
        effects_symptoms={"Cognitive Decline": "reveal", "Memory Loss": "alleviate"}  # Revela declive cognitivo
    ),
    Procedure(
        name="Speech Therapy",
        cost=200,
        effects_progress=10,
        effects_symptoms={"Difficulty Speaking": "alleviate"}  # Revela bradicinesia
    ),
    Procedure(
        name="Surgery for Severe Cases",
        cost=500,
        effects_progress=30,
        effects_symptoms={"Heart Problems": "alleviate", "Involuntary Movements": "alleviate"}  # Mantiene alivio para problemas graves
    ),
    Procedure(
        name="Augmentative Communication Devices",
        cost=800,
        effects_progress=15,
        effects_symptoms={"Difficulty Speaking": "alleviate", "Cognitive Decline": "reveal"}  # Revela declive cognitivo
    ),
    Procedure(
        name="Cognitive Behavioral Therapy",
        cost=350,
        effects_progress=10,
        effects_symptoms={"Mood Changes": "alleviate", "Memory Loss": "reveal"}  # Revela pérdida de memoria
    ),
    Procedure(
        name="Supportive Therapy",
        cost=200,
        effects_progress=5,
        effects_symptoms={ "Mood Changes": "alleviate"}  
    ),
    Procedure(
        name="Cognitive Therapies",
        cost=300,
        effects_progress=5,
        effects_symptoms={"Cognitive Decline": "reveal", "Memory Loss": "alleviate"}
    ),
    Procedure(
        name="Assistive Devices like Walkers",
        cost=500,
        effects_progress=10,
        effects_symptoms={"Difficulty Walking": "alleviate", "Muscle Weakness": "reveal"}
    ),
    Procedure(
        name="Pain Management Therapies",
        cost=400,
        effects_progress=10,
        effects_symptoms={"Numbness or Tingling": "alleviate", "Muscle Weakness": "reveal"}  
    ),
    Procedure(
        name="Physical Therapy",
        cost=250,
        effects_progress=20,
        effects_symptoms={ "Muscle Weakness": "alleviate", "Difficulty Walking": "alleviate"}  
    ),
    Procedure(
        name="Psychotherapy",
        cost=300,
        effects_progress=15,
        effects_symptoms={"Mood Changes": "alleviate"}  
    ),
    Procedure(
        name="Surgery in Refractory Cases",
        cost=700,
        effects_progress=40,
        effects_symptoms={"Seizures": "alleviate"} 
    ),
    Procedure(
        name="Lifestyle Changes",
        cost=100,
        effects_progress=20,
        effects_symptoms={"Fatigue": "reveal", "Mood Changes": "alleviate"}
    )
]


treatment_medications = [
    Medication(
        name="Cholinesterase Inhibitors",
        dosage=1,
        duration=30,
        effects_progress=15,
        effects_symptoms={"Cognitive Decline": "alleviate", "Memory Loss": "alleviate"}
    ),
    Medication(
        name="Medications to Manage Symptoms",
        dosage=1,
        duration=15,
        effects_progress=10,
        effects_symptoms={"Fatigue": "alleviate", "Mood Changes": "alleviate"}
    ),
    Medication(
        name="Medications like Beta-Blockers",
        dosage=1,
        duration=30,
        effects_progress=20,
        effects_symptoms={"Heart Problems": "alleviate"}
    ),
    Medication(
        name="Antipsychotic Medications",
        dosage=1,
        duration=30,
        effects_progress=25,
        effects_symptoms={"Visual Hallucinations": "alleviate", "Mood Changes": "alleviate"}
    ),
    Medication(
        name="Medications to Slow Progression",
        dosage=1,
        duration=60,
        effects_progress=30,
        effects_symptoms={"Cognitive Decline": "alleviate", "Bradykinesia": "alleviate"}
    ),
    Medication(
        name="Medications for Nerve Pain",
        dosage=1,
        duration=20,
        effects_progress=15,
        effects_symptoms={"Numbness or Tingling": "alleviate"}
    ),
    Medication(
        name="Levodopa Medication",
        dosage=1,
        duration=30,
        effects_progress=40,
        effects_symptoms={"Tremor": "alleviate", "Bradykinesia": "alleviate"}
    ),
    Medication(
        name="Medications such as Antidepressants",
        dosage=1,
        duration=30,
        effects_progress=20,
        effects_symptoms={"Mood Changes": "alleviate"}
    ),
    Medication(
        name="Antiepileptic Medications",
        dosage=1,
        duration=30,
        effects_progress=15,
        effects_symptoms={"Seizures": "alleviate"}
    ),
    Medication(
        name="Medications for Heart Health",
        dosage=1,
        duration=30,
        effects_progress=25,
        effects_symptoms={"Heart Problems": "alleviate"}
    )
]

