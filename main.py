import json
from A_Star_Algorithim import A_Star, Support, Goal
from Language import chat
from Knowledge.disease_detection import DiseasePredictionModel

with open("Knowledge/ontology.json", 'r') as file:
    ontology = json.load(file)

database_path = "Knowledge/patient_data.csv"

# Crear el modelo de predicción
model = DiseasePredictionModel(ontology, database_path)

# Entrenar el modelo
model.train_model()

# Hacer la predicción
patient, history = chat.chating("Imagine you are the Christina Yang from Grey's Anatomy")

energy_level = chat.analyze_conversation(history, "nivel de energía")
pain_level = chat.analyze_conversation(history, "nivel de dolor")

patient_symptoms = [s.name for s in patient.symptoms]

prediction = model.predict_disease(patient_symptoms)

#! !!!!!!!!!!!!!!!!!!Hay que extraerlas del ontology.json !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#! ["Brain Cancer", "Encephalitis", "Epilepsy", "Multiple Sclerosis", "Prion Diseases",
#!                 "Spinal Muscular Atrophy", "Parkinson's Disease", "Lewy Body Dementia", 
#!                 "Huntington's Disease", "Friedreich's Ataxia", "Amyotrophic Lateral Sclerosis", "Alzheimer's Disease"]
#!
#! ["Memory Loss", "Muscle Weakness", "Involuntary Movements", "Tremor", "Difficulty Speaking", 
#!                  "Fatigue", "Visual Hallucinations", "Cognitive Decline", "Difficulty Walking", 
#!                  "Numbness or Tingling", "Bradykinesia", "Mood Changes", "Seizures", "Heart Problems"]

# Generar el array de enfermedades activas
active_diseaes = [[clave for clave, valor in prediction.items() if valor > 0]]

# Verificar si hay enfermedades activas
if not active_diseaes:
    active_diseaes = ["No hay enfermedades"]

print()
print(f"Predicted Disease:")
for clave, valor in prediction.items():
        if valor == 0: break
        print(f"{clave.name}: {valor}%")
print()



# Define the list of possible procedures
possible_procedures = [
    Support.Procedure(
        name="MRI Scan", 
        cost=500, 
        effects_progress=-5,  
        effects_symptoms={"Atrophy": "reveal"}  
    ),
    Support.Procedure(
        name="Blood Test", 
        cost=100, 
        effects_progress=0, 
        effects_symptoms={"B12 Deficiency": "reveal"}  
    )
]


# Define the list of possible medications
possible_medications = [
    Support.Medication(
        name="Painkiller", 
        dosage=1, 
        duration=7, 
        effects_progress=10,  
        effects_symptoms={"headache": "alleviate"}  
    ),
    Support.Medication(
        name="Vitamin B12", 
        dosage=1, 
        duration=30, 
        effects_progress=30,  
        effects_symptoms={"fatigue": "alleviate"}  
    )
]       


# Initialize the AStar object with the possible procedures and medications
astar = A_Star.AStar(possible_procedures, possible_medications)

# Create an initial state for the patient
initial_state = A_Star.State(
    medications=[],  
    procedures=[],  
    symptoms=[Support.Symptom(s, "severe") for s in patient_symptoms],
    progress=Support.Progress(30),  # The patient starts with 30% progress
    general_state=Support.StateGeneral(energy_level, pain_level, immune_status="weak")
)


# Run the A* search algorithm
solution = astar.a_star(initial_state, Goal.GoalCheck.is_goal)

abstract = chat.abstract(history, str(patient), astar.log)
print(abstract)

