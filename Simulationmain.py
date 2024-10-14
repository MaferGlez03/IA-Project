import json
import simpy
import random
import itertools
from Tests import most_used_service
from Language import chat
from Knowledge.disease_detection import DiseasePredictionModel
from Simulation import Doctor, Patient, Hospital, Procedures, Tools
from A_Star_Algorithim import A_Star,Support

results=[]
def doctor(env, procedures, model, hospital, id, threshold=0):
    sim_time = env.now + 1000
    #! Cambiar tiempo espera hasta que todas las enfermedades esten por debajo del nivel esperado
    while env.now < sim_time:
        if not hospital.patients:
            yield env.timeout(5)
            continue
        patient = hospital.take_patient()

        beliefs = Doctor.beliefs(patient.symptoms, model)
        desires = Doctor.desires(beliefs, threshold)

        intentions = []

        while patient.disease_progress >= threshold: 

            if intentions:
                if "can be discharged" in " ".join([intention[0] for intention in intentions]): # Modificar para que en algun momento termine con el paciente
                    yield env.timeout(random.randint(1, 3))
                    break
            
            Doctor.brf(beliefs, patient.symptoms, model)
            Doctor.generate_options(beliefs, patient.symptoms, procedures, desires)
            intentions = Doctor.filter(beliefs, desires, patient)

            if not intentions:
                yield env.timeout(10)
                continue            

            env.process(Doctor.execute_action(intentions, patient, procedures,results,env, desires, beliefs))
            
            yield env.timeout(random.randint(1, 3))

def patients(env, hospital, id, patient, threshold):
    perception = {
        
    }

    beliefs = Patient.beliefs(patient)
    desires = Patient.desires()

    patient.set_disease_progress(beliefs['disease_progress'])

    while env.now < 100:
        Patient.brf(perception, beliefs, patient)
        Patient.generate_option(beliefs, desires, threshold)
        Patient.filter(beliefs, desires)

        env.process(Patient.execute_action(hospital, beliefs, desires, perception, results, env, patient))
        yield env.timeout(random.randint(1, 3))
        if beliefs['has_left']: return
    
    
def patient_generator(env, model, hospital, threshold):
    """Generate new patients that arrive at the hospital."""
    for i in itertools.count():
        yield env.timeout(random.randint(*[5,20]))

        # Hacer la predicción
        patient, history = chat.chating("Christina Yang from Grey's Anatomy")

        hospital.patients.append(patient)

        energy_level = chat.analyze_conversation(history, "nivel de energía")
        pain_level = chat.analyze_conversation(history, "nivel de dolor")
        patient.energy_level=energy_level
        patient.pain_level=pain_level
        env.process(patients(env, hospital, i, patient))

        

        
        env.process(patients(env, hospital, i, patient, threshold))

        patient_symptoms = [s.name for s in patient.symptoms]

        prediction = model.predict_disease(patient_symptoms)
        patient.diseases = prediction
        results.append((env.now, f'Patient {patient.name} has been ingressed with a possible {list(prediction.keys())[0].name}'))

        print()
        print(f"Predicted Disease:")
        for clave, valor in prediction.items():
                if valor == 0: break
                print(f"{clave.name}: {valor}%")
        print()


    
    

def create_model():
    with open("Knowledge/ontology.json", 'r') as file:
        ontology = json.load(file)

    database_path = "Knowledge/patient_data.csv"

    # Crear el modelo de predicción
    model = DiseasePredictionModel(ontology, database_path)

    # Entrenar el modelo
    model.train_model()    

    return model

def run_simulation(threshold=15):
    env = simpy.Environment()
    procedures = Procedures.create_procedures()
    results.append((env.now,'Hospital is open'))

    hospital = Hospital.Hospital(env, procedures)

    model = create_model()

    env.process(patient_generator(env, model, hospital, threshold))
    for i in range(5):
        env.process(doctor(env, procedures, model, hospital, i, threshold))
        env.timeout(1)

    

    env.run(until=40)
    Tools.save_log(results)
    return hospital

data = most_used_service.test_procedures(run_simulation)
most_used_service.graphs(data, 0)
most_used_service.graphs(data, 1)
# run_simulation()


#! !!!!!!!!!!!!!!!!!!Hay que extraerlas del ontology.json !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#! ["Brain Cancer", "Encephalitis", "Epilepsy", "Multiple Sclerosis", "Prion Diseases",
#!                 "Spinal Muscular Atrophy", "Parkinson's Disease", "Lewy Body Dementia", 
#!                 "Huntington's Disease", "Friedreich's Ataxia", "Amyotrophic Lateral Sclerosis", "Alzheimer's Disease"]
#!
#! ["Memory Loss", "Muscle Weakness", "Involuntary Movements", "Tremor", "Difficulty Speaking", 
#!                  "Fatigue", "Visual Hallucinations", "Cognitive Decline", "Difficulty Walking", 
#!                  "Numbness or Tingling", "Bradykinesia", "Mood Changes", "Seizures", "Heart Problems"]