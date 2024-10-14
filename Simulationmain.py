import json
import simpy
import random
import itertools
from Language import chat
from Knowledge.disease_detection import DiseasePredictionModel
from Simulation import Doctor, Patient, Hospital, Procedures, Tools
from A_Star_Algorithim import A_Star,Support

results=[]
def doctor(env, procedures, model, hospital, id, disease_level=0):
    sim_time = env.now + 1000
    #! Cambiar tiempo espera hasta que todas las enfermedades esten por debajo del nivel esperado
    while env.now < sim_time:
        if not hospital.patients:
            yield env.timeout(5)
            continue
        print(f"New patient Doctor {id}")
        patient = hospital.take_patient()

        while patient.disease_progress >= disease_level: 
            print(f"BDI Doctor {id}")

            beliefs = Doctor.beliefs(patient.symptoms, model)
            desires = Doctor.desires(beliefs)
            
            Doctor.brf(beliefs, patient.symptoms, model)
            Doctor.generate_options(beliefs, patient.symptoms, procedures, desires)
            intentions = Doctor.filter(beliefs, desires, patient)

            if not intentions:
                print(f"Not intentions Doctor {id}")
                yield env.timeout(10)
                continue            

            env.process(Doctor.execute_action(intentions, patient, procedures,results,env, desires, beliefs))
            
            if "can be discharged" in " ".join([intention[0] for intention in intentions]): # Modificar para que en algun momento termine con el paciente
                print(f"Next Patient Doctor {id}")
                yield env.timeout(random.randint(1, 3))
                break
            
            yield env.timeout(random.randint(1, 3))

def patients(env, hospital, id, patient):
    perception = {
        
    }

    beliefs = Patient.beliefs(patient)
    desires = Patient.desires()

    patient.set_disease_progress(beliefs['disease_progress'])

    while env.now < 100:
        print()
        print("BDI patient")
        print(patient.name)
        print(patient.disease_progress)
        print()
        Patient.brf(perception, beliefs, patient)
        Patient.generate_option(beliefs, desires)
        Patient.filter(beliefs, desires)

        
        env.process(Patient.execute_action(hospital, beliefs, desires, perception, results, env, patient))
        yield env.timeout(random.randint(1, 3))
        if beliefs['has_left']: return
    
    
def patient_generator(env, model, hospital):
    """Generate new patients that arrive at the hospital."""
    for i in itertools.count():
        yield env.timeout(random.randint(*[5,20]))

        # Hacer la predicción
        patient, history = chat.chating("Christina Yang from Grey's Anatomy")

        hospital.patients.append(patient)

        env.process(patients(env, hospital, i, patient))

        

        # energy_level = chat.analyze_conversation(history, "nivel de energía")
        # pain_level = chat.analyze_conversation(history, "nivel de dolor")

        patient_symptoms = [s.name for s in patient.symptoms]

        prediction = model.predict_disease(patient_symptoms)
        results.append((env.now, f'Patient {patient.name} has been ingressed with a possible {list(prediction.keys())[0].name}'))

        print()
        print(f"Predicted Disease:")
        for clave, valor in prediction.items():
                if valor == 0: break
                print(f"{clave.name}: {valor}%")
        print()

def apply_A_Star(patient, goal):
    # Initialize the AStar object with the possible procedures and medications
    astar = A_Star.AStar()
    initial_state = A_Star.State(
    medications=[],  
    procedures=[],  
    symptoms=[Support.Symptom(s, "severe") for s in patient.symptoms.name],
    progress=Support.Progress(patient.disease_progress),  # The patient starts with 30% progress
    general_state=Support.StateGeneral(patient.energy_level, patient.pain_level, immune_status="weak")
    )
    solution = astar.a_star(initial_state, goal)
    if solution :return solution.medications.extend(solution.procedures)
    return []
    
    return hospital

def create_model():
    with open("Knowledge/ontology.json", 'r') as file:
        ontology = json.load(file)

    database_path = "Knowledge/patient_data.csv"

    # Crear el modelo de predicción
    model = DiseasePredictionModel(ontology, database_path)

    # Entrenar el modelo
    model.train_model()    

    return model

def run_simulation(progress_disease_level=10):
    env = simpy.Environment()
    procedures = Procedures.create_procedures()
    results.append((env.now,'Hospital is open'))

    hospital = Hospital.Hospital(env, procedures)

    model = create_model()

    env.process(patient_generator(env, model, hospital))
    for i in range(5):
        env.process(doctor(env, procedures, model, hospital, i))
        env.timeout(1)

    

    env.run(until=100)
    Tools.save_log(results)

run_simulation()