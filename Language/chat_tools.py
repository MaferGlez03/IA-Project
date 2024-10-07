import re
import json
from Knowledge import medical_record

print("cero")

with open("Knowledge/ontology.json", 'r') as file:
    ontology = json.load(file)
    
print("uno")
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

# Lista de síntomas conocidos
# KNOWN_SYMPTOMS = {
#     "memory loss": medical_record.Symptom("s1", "Memory Loss", "A decline in the ability to remember information, which can affect daily life.", ["Alzheimer's", "Lewy body dementia", "Huntington's"], ["Cognitive therapy", "Cholinesterase inhibitors"], ["Cognitive assessments", "Neuroimaging"]),
#     "muscle weakness": medical_record.Symptom("s2", "Muscle Weakness", "A condition characterized by a decrease in muscle strength, affecting mobility and daily activities.", ["ALS", "Spinal muscular atrophy", "Friedreich's ataxia"], ["Physical therapy", "Medications to manage symptoms"], ["Electromyography (EMG)", "Muscle biopsy"]),
#     "involuntary movements": medical_record.Symptom("s3", "Involuntary Movements", "Uncontrolled movements that can include jerks, twitches, or spasms.", ["Huntington's", "Parkinson's"], ["Antipsychotic medications", "Physical therapy"], ["Neurological examination", "MRI"]),
#     "tremor": medical_record.Symptom("s4", "Tremor", "Rhythmic shaking of a part of the body, often observed in the hands.", ["Essential tremor", "Parkinson's"], ["Medications like beta-blockers",  "Surgery for severe cases"], ["Neurological examination", "Blood tests to rule out other causes"]),
#     "difficulty speaking": medical_record.Symptom("s5", "Difficulty Speaking", "Challenges in articulating words or forming sentences, often leading to frustration.", ["ALS", "Parkinson's", "Multiple sclerosis"], ["Speech therapy", "Augmentative communication devices"], ["Speech assessments", "Neurological evaluations"]),
#     "fatigue": medical_record.Symptom("s6", "Fatigue", "A feeling of tiredness or lack of energy that is persistent and not alleviated by rest.", ["Multiple sclerosis", "Parkinson's"], ["Cognitive behavioral therapy", "Medications"], ["Blood tests to check for anemia or thyroid issues", "Sleep studies"]),
#     "visual hallucinations": medical_record.Symptom("s7", "Visual Hallucinations", "Seeing things that are not present, often associated with cognitive disorders.", ["Lewy body dementia", "Parkinson's disease"], ["Antipsychotic medications", "Supportive therapy"], ["Neurological assessments", "Psychiatric evaluations"]),
#     "rigidez muscular": medical_record.Symptom("s8", "Rigidez muscular", "Tensión o endurecimiento de los músculos", ["Parkinson's", "Esclerosis lateral amiotrófica (ELA)"], ["Medicamentos relajantes musculares"], ["Examen físico", "Pruebas neurológicas"]),
#  #!   "pérdida de memoria": medical_record.Symptom("s9", "Pérdida de memoria", "Dificultad para recordar información reciente", ["Alzheimer's", "Demencia"], ["Ejercicios cognitivos", "Medicamentos como Donepezilo"], ["Resonancia magnética", "Evaluación neuropsicológica"]),
#     "trastornos del habla": medical_record.Symptom("s10", "Trastornos del habla", "Dificultad para hablar o encontrar palabras", ["Esclerosis múltiple", "Demencia frontotemporal"], ["Terapia del habla"], ["Evaluación cognitiva"]),
#     "dificultad para caminar": medical_record.Symptom("s11", "Dificultad para caminar", "Problemas de movilidad", ["Esclerosis múltiple", "Ataxia espinocerebelosa"], ["Fisioterapia", "Ayudas de movilidad"], ["Estudios de imagen", "Exámenes neurológicos"]),
#     "movimientos involuntarios": medical_record.Symptom("s12", "Movimientos involuntarios", "Movimientos anormales y no controlados", ["Corea de Huntington", "Distonía"], ["Medicamentos antiespasmódicos"], ["Pruebas genéticas", "Evaluación neurológica"]),
#     "apatía": medical_record.Symptom("s13", "Apatía", "Falta de interés o motivación", ["Alzheimer's", "Demencia frontotemporal"], ["Terapia ocupacional", "Apoyo psicológico"], ["Evaluación neuropsicológica"]),
#     "pérdida de equilibrio": medical_record.Symptom("s14", "Pérdida de equilibrio", "Inestabilidad al caminar o estar de pie", ["Esclerosis múltiple", "Ataxia"], ["Fisioterapia", "Ejercicios de equilibrio"], ["Pruebas de función motora"]),
#     "dificultad para tragar": medical_record.Symptom("s15", "Dificultad para tragar", "Problemas para ingerir alimentos o líquidos", ["ELA", "Parkinson's"], ["Terapia de deglución", "Cambios en la dieta"], ["Videofluoroscopia", "Evaluación clínica"]),
#     "incontinencia urinaria": medical_record.Symptom("s16", "Incontinencia urinaria", "Pérdida involuntaria de orina", ["Esclerosis múltiple", "Demencia avanzada"], ["Medicamentos", "Fisioterapia del suelo pélvico"], ["Urodinamia", "Exámenes físicos"]),
#     "cambios en el estado de ánimo": medical_record.Symptom("s17", "Cambios en el estado de ánimo", "Fluctuaciones extremas de humor", ["Demencia", "Huntington's"], ["Apoyo psicológico", "Medicamentos estabilizadores del ánimo"], ["Evaluación psiquiátrica"]),
#     "visión borrosa": medical_record.Symptom("s18", "Visión borrosa", "Dificultad para ver con claridad", ["Esclerosis múltiple", "Degeneración macular"], ["Tratamientos oftalmológicos"], ["Evaluación ocular", "Resonancia magnética"]),
#     "deterioro cognitivo": medical_record.Symptom("s19", "Deterioro cognitivo", "Pérdida gradual de funciones mentales", ["Alzheimer's", "Demencia vascular"], ["Ejercicios cognitivos", "Tratamientos farmacológicos"], ["Evaluaciones neuropsicológicas", "Resonancia magnética"]),
#     "alucinaciones": medical_record.Symptom("s20", "Alucinaciones", "Percepción de cosas que no están presentes", ["Demencia con cuerpos de Lewy", "Parkinson's avanzado"], ["Antipsicóticos", "Monitoreo médico"], ["Evaluaciones neuropsiquiátricas"]),
#     "movimientos espasmódicos": medical_record.Symptom("s21", "Movimientos espasmódicos", "Contracciones musculares rápidas e involuntarias", ["Huntington's", "Corea"], ["Medicamentos para los espasmos"], ["Pruebas genéticas", "Electromiografía"]),
#     "dificultad para concentrarse": medical_record.Symptom("s22", "Dificultad para concentrarse", "Problemas para mantener la atención", ["Alzheimer's", "Esclerosis múltiple"], ["Ejercicios cognitivos", "Terapias ocupacionales"], ["Evaluación neuropsicológica"]),
# }


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

