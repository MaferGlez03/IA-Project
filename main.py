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

patient_info = {
    'age': int(patient.age),
    'lifestyle_factors1': 1,
    'lifestyle_factors2': 1,
    'lifestyle_factors3': 1,
    'lifestyle_factors4': 1,
    'lifestyle_factors5': 1,
    'lifestyle_factors6': 1,
    'lifestyle_factors7': 1,
    'lifestyle_factors8': 1,
    'lifestyle_factors9': 1,
    'lifestyle_factors10': 1,
    'lifestyle_factors11': 1,
    'lifestyle_factors12': 1,
    'family_history1': 1,
    'family_history2': 1,
    'family_history3': 1,
    'family_history4': 1,
    'family_history5': 1,
    'family_history6': 1,
    'family_history7': 1,
    'family_history8': 1,
    'family_history9': 1,
    'family_history10': 1,
    'family_history11': 1,
    'family_history12': 1,
    'genetic_predisposition1': 1,
    'genetic_predisposition2': 1,
    'genetic_predisposition3': 1,
    'genetic_predisposition4': 1,
    'genetic_predisposition5': 1,
    'genetic_predisposition6': 1,
    'genetic_predisposition7': 1,
    'genetic_predisposition8': 1,
    'genetic_predisposition9': 1,
    'genetic_predisposition10': 1,
    'genetic_predisposition11': 1,
    'genetic_predisposition12': 1,
    'environmental_exposure1': 1,
    'environmental_exposure2': 1,
    'environmental_exposure3': 1,
    'environmental_exposure4': 1,
    'environmental_exposure5': 1,
    'environmental_exposure6': 1,
    'environmental_exposure7': 1,
    'environmental_exposure8': 1,
    'environmental_exposure9': 1,
    'environmental_exposure10': 1,
    'environmental_exposure11': 1,
    'environmental_exposure12': 1
}
patient_symptoms = patient.symptoms


prediction = model.predict(patient_symptoms, patient_info)

#! !!!!!!!!!!!!!!!!!!Hay que extraerlas del ontology.json !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
diseaes = ["Brain Cancer", "Encephalitis", "Epilepsy", "Multiple Sclerosis", "Prion Diseases",
                "Spinal Muscular Atrophy", "Parkinson's Disease", "Lewy Body Dementia", 
                "Huntington's Disease", "Friedreich's Ataxia", "Amyotrophic Lateral Sclerosis", "Alzheimer's Disease"]

# Generar el array de enfermedades activas
active_diseaes = [enfermedad for enfermedad, activo in zip(diseaes, prediction) if activo == 1]

# Verificar si hay enfermedades activas
if not active_diseaes:
    active_diseaes = ["No hay enfermedades"]

# Resultado
print(f"{active_diseaes}\n\n\n\n")

# print(f"Predicted Disease: {prediction}")




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
    symptoms=[Support.Symptom(s.name, "severe") for s in patient_symptoms],
    progress=Support.Progress(30),  # The patient starts with 30% progress
    general_state=Support.StateGeneral(energy_level, pain_level, immune_status="weak")
)


# Run the A* search algorithm
solution = astar.a_star(initial_state, Goal.GoalCheck.is_goal)

abstract = chat.abstract(history, str(patient), astar.log)
print(abstract)

