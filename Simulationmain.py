import json
import simpy
import random
import itertools
from Language import chat
from Knowledge.disease_detection import DiseasePredictionModel
from Simulation import Doctor, Patient, Hospital
results=[]
def doctor(env, beliefs, desires, sim_time, procedures, patient_symptoms, model, patient):
    #! Cambiar tiempo espera hasta que todas las enfermedades esten por debajo del nivel esperado
    while env.now < sim_time: 
        print("Start Doc")
        Doctor.brf(beliefs, patient_symptoms, model)
        Doctor.generate_options(beliefs, patient_symptoms, procedures, desires)
        intentions = Doctor.filter(beliefs, desires, patient)

        if not intentions:
            yield env.timeout(10)
            continue
        print(intentions)
        print(patient)
        print([procedure.name for procedure in procedures])
        env.process(Doctor.execute_action(intentions, patient, procedures,results,env))
        yield env.timeout(random.randint(1, 3))
    print("End Doc")

def patients(env, beliefs, desires, hospital, id):
    perception = {
        
    }

    while env.now < 100:
        Patient.brf(perception, beliefs)
        Patient.generate_option(beliefs, desires)
        intentions = Patient.filter(beliefs, desires)

        if not intentions:
            yield env.timeout(10)
            continue  
        env.process(Patient.execute_action(hospital, beliefs, desires, perception))
        if beliefs['has_left']: return
        yield env.timeout(random.randint(1, 3))
    
    hospital.patients[id] = beliefs
    
def patient_generator(env, hospital, procedures):
    """Generate new tourists that arrive at the hotel."""
    for i in itertools.count():
        yield env.timeout(random.randint(*[5,20 ]))
        env.process(patients(env, Patient.beliefs(), Patient.desires(), hospital, i))
        
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

        beliefs = Doctor.beliefs(patient_symptoms, model)

        print()
        print(f"Predicted Disease:")
        for clave, valor in prediction.items():
                if valor == 0: break
                print(f"{clave.name}: {valor}%")
        print()

        env.process(doctor(env, beliefs, Doctor.desires(beliefs), env.now + 100, procedures, patient_symptoms, model, patient))

def create_procedures():
    
    procedures = []
    procedures.append(Hospital.Procedure("Huntington_Disease", "u1", "f1", "r1"))
    return procedures

def run_simulation():
    env = simpy.Environment()
    procedures = create_procedures()
    results.append((env.now,'Hospital is open'))

    hospital = Hospital.Hospital(env, procedures)

    env.process(patient_generator(env, hospital, procedures))

    env.run(until=100)

run_simulation()