import re
import json
from Knowledge import medical_record

with open("Knowledge/ontology.json", 'r') as file:
    ontology = json.load(file)

# Crear un diccionario para almacenar los síntomas
KNOWN_SYMPTOMS = {}

# Iterar sobre la lista de síntomas en el JSON
for symptom in ontology.get('symptoms', []):
    id = symptom['id']
    name = symptom['name'].lower()  # Convertir el nombre del síntoma a minúsculas
    description = symptom['description']
    associated_diseases = symptom['associated_diseases']
    treatments = symptom['treatments']
    diagnostic_tests = symptom['diagnostic_tests']
    
    # Crear el objeto Symptom y añadirlo al diccionario
    KNOWN_SYMPTOMS[name] = medical_record.Symptom(
        id=id,
        name=symptom['name'],
        description=description,
        associated_diseases=associated_diseases,
        treatments=treatments,
        diagnostic_tests=diagnostic_tests
    )

def identify_symptoms(text):
    
    # Convertir el texto a minúsculas y eliminar signos de puntuación
    text_clean = re.sub(r'[^\w\s]', '', text.lower())

    # Crear una lista para almacenar los síntomas identificados
    identified_symptoms = []

    # Buscar cada síntoma conocido en el texto
    for symptom_name, symptom in KNOWN_SYMPTOMS.items():
        if symptom_name in text_clean:
            if symptom_name in identified_symptoms: continue
            identified_symptoms.append(symptom)

    return identified_symptoms

