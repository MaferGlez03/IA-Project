import os
import random
import time
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv
from Knowledge.medical_record import Patient
from Language.chat_tools import identify_symptoms

def configure_model(user_system_instruction=""):
    """
    Configura y devuelve una instancia del modelo generativo de Google.
    """
    # Cargar las variables de entorno
    load_dotenv()

    # Configurar la API de Google Generative AI
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    # Crear la configuración del modelo
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Crear y devolver el modelo generativo
    if user_system_instruction:
      model = genai.GenerativeModel(
          model_name="gemini-1.5-flash",
          generation_config=generation_config,
          safety_settings={
              HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
              HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
              HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
              HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
          },
          system_instruction = user_system_instruction
      )
    else:
        model = genai.GenerativeModel(
          model_name="gemini-1.5-flash",
          generation_config=generation_config,
          safety_settings={
              HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
              HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
              HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
              HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
          },
      )
    return model

def analyze_conversation(history, analysis_target="nivel de enfermedad"):
    """
    Función para analizar el historial de la conversación y obtener una deducción basada en la misma.
    :param model: Instancia del modelo generativo.
    :param history: Lista que contiene el historial del chat.
    :param analysis_target: El objetivo del análisis (ej. nivel de enfermedad, gravedad, etc.).
    """
    # Obtener la instancia del modelo generativo
    model = configure_model()
    
    # Convertir el historial a un formato de texto para ser enviado como entrada
    conversation_text = "\n".join([f"{turn['role']}: {' '.join(turn['parts'])}" for turn in history])

    # Formar la consulta con el historial y el objetivo del análisis
    prompt = f"Basado en la siguiente conversación, determina el {analysis_target} del paciente. Responde solo con un numero del 0 al 10.\n\n{conversation_text}"

    # Generar respuesta del modelo
    chat_session = model.start_chat()
    response = chat_session.send_message(prompt)
    
    print(f"{analysis_target}: {convert_to_int_or_zero(response.text)}") #! ***************************************************
    return convert_to_int_or_zero(response.text)

def chating(role): # Imagine you are the Christina Yang from Grey's Anatomy
    # Obtener la instancia del modelo generativo
    model_doctor = configure_model(f"{role}, you are in a neurodegenerative disease center and I need you to determine in 5 interactions what disease the patient may have. In order to record the symptoms, I need you to invite the patient to mention the symptom explicitly. Only english")
    model_patient = configure_model(f"You are a patient suffering from a neurodegenerative disease. You are currently in a doctor's office for a consultation. Your task is to respond to the doctor's questions about your symptoms in detail. Please behave naturally and realistically as a patient would during such a consultation. Please begin by describing your current state and any immediate concerns you have.After receiving the doctor's questions, respond accordingly, then wait for the next question.Remember to describe your symptoms honestly and explicitly, as if you were actually experiencing them. Repeat this process for a total of 5 exchanges. After the fifth exchange, please say goodbye to end the simulation. Only english")
    
    history = []

    # Listas de nombres y apellidos
    first_names = [
        "Carlos", "María", "Juan", "Ana", "José", "Luis", "Sofía", "Laura", "David", "Pedro", "Marta", "Jorge", "Lucía", "Fernando", "Andrés", "Paula", "Camila", "Diego", "Gabriela", "Miguel",
        "Adriana", "Raúl", "Isabel", "Manuel", "Carmen", "Roberto", "Francisco", "Alba", "Santiago", "Beatriz", "Enrique", "Eva", "Alberto", "Irene", "Cristina", "Elena", "Julio", "Esteban", 
        "Teresa", "Héctor", "Marcos", "Rosa", "Álvaro", "Natalia", "Patricia", "Guillermo", "Daniel", "Silvia", "Sebastián", "Pablo", "Inés", "Estefanía", "Ricardo", "Victoria", "Federico", 
        "Claudia", "Fabián", "Tomás", "Alicia", "Marcelo", "Emilio", "Diana", "Rubén", "Ángela", "Bruno", "Valeria", "Mateo", "Antonia", "César", "Julia", "Renata", "Nicolás", "Sara", "Mario",
        "Clara", "Félix", "Agustín", "Olga", "Rodrigo", "Verónica", "Sergio", "Emilia", "Gustavo", "Cecilia", "Mauricio", "Rafael", "Gloria", "Iván", "Samantha", "Jaime", "Lola", "Álex", 
        "Cristóbal", "Ignacio", "Noelia", "Estrella", "Edgar", "Mariano", "Fátima", "Raimundo", "Lourdes", "Ágata", "Ezequiel", "Montserrat"
    ]

    last_names = [
        "García", "Rodríguez", "Martínez", "Hernández", "López", "González", "Pérez", "Sánchez", "Ramírez", "Torres", "Flores", "Castro", "Rivas", "Ortega", "Molina", "Vargas", "Morales", 
        "Reyes", "Iglesias", "Paredes", "Domínguez", "Chávez", "Ramos", "Vega", "Cruz", "Silva", "Núñez", "Cortés", "Esquivel", "Zamora", "Vázquez", "Delgado", "Sosa", "Peña", "Mejía", "Salinas", 
        "Suárez", "Luna", "Cabrera", "Ornelas", "Méndez", "Medina", "Durán", "Arias", "Blanco", "Carrillo", "León", "Calderón", "Fernández", "Ortiz", "Montoya", "Miranda", "Muñoz", "Cano", 
        "Herrera", "Rangel", "Valdez", "Quintana", "Aguilar", "Juárez", "Salazar", "Lara", "Villanueva", "Ruiz", "Valencia", "Alvarado", "Ponce", "Benítez", "Solís", "Santana", "Cuevas", "Maldonado", 
        "Rojas", "Escobar", "Guerrero", "Bravo", "Figueroa", "Pizarro", "Acosta", "Espinoza", "Pineda", "Palacios", "Romero", "Fuentes", "Ochoa", "Domingo", "Mora", "Roldán", "Beltrán", "Jiménez", 
        "Zúñiga", "Paredes", "Hidalgo", "Arroyo", "Olivares", "Montero", "Camacho", "Bautista", "Villarreal", "Galindo", "Prieto", "Mansilla", "Varela", "Escamilla", "Bustamante", "Barrios", "Sepúlveda"
    ]

    name = random.choice(first_names) + " " + random.choice(last_names) + " " + random.choice(last_names)
    age = random.randint(18, 100)
    sex = random.choice(["Male", "Female"])
    print()

    # Crear un paciente
    patient = Patient(name, age, sex)

    doctor_response = "Hello, how can I help you today?"
    
    print("Doctor: " + doctor_response)
    print()

    for _ in range(5):  # Limitar a 5 interacciones
        # Respuesta del paciente (IA)
        chat_patient = model_patient.start_chat(history=history)
        try:
           patient_response = chat_patient.send_message(doctor_response.text)
        except:
            patient_response = chat_patient.send_message(doctor_response)

        # Identificar síntomas en la respuesta del paciente
        symptoms_found = identify_symptoms(patient_response.text)

        # Añadir los síntomas identificados al paciente
        for symptom in symptoms_found:
            patient.add_symptom(symptom)

        # Mostrar respuesta del paciente
        print(f"Paciente: {patient_response.text}")
        print()

        # Añadir la respuesta a la historia
        history.append({"role": "user", "parts": [patient_response.text]})

        time.sleep(5)

        # Respuesta del doctor (IA)
        chat_doctor = model_doctor.start_chat(history=history)
        doctor_response = chat_doctor.send_message(patient_response.text)

        # Mostrar respuesta del doctor
        print(f"Doctor: {doctor_response.text}")
        print()

        # Almacenar la respuesta del doctor en la historia
        history.append({"role": "model", "parts": [doctor_response.text]})

        # Terminar la conversación si se detecta que el paciente termina
        if "bye" in patient_response.text.lower():
            break

        time.sleep(5)

    # Imprimir la información del paciente
    print()
    print(patient)
    return patient, history

def convert_to_int_or_zero(value):
    try:
        # Intentar convertir a int
        return int(value)
    except ValueError:
        # Si ocurre ValueError, retornar 0
        return 0

def abstract(patient_interview, diagnosis, patient_monitoring):
     # Obtener la instancia del modelo generativo
    model = configure_model()
    
    # Convertir la entrevista con el paciente a un formato de texto para ser enviado como entrada
    phase1 = "\n".join([f"{turn['role']}: {' '.join(turn['parts'])}" for turn in patient_interview])

    # Convertir el diagnostico a un formato de texto para ser enviado como entrada
    phase2 = "\n".join({"role": "model", "parts": [diagnosis]})

    # Convertir el seguimiento al paciente a un formato de texto para ser enviado como entrada
    phase3 = "\n".join({"role": "model", "parts": [patient_monitoring]})

     # Formar la consulta con el historial y el objetivo del análisis
    prompt = f"Crea un resumen medico formal de todo lo que vas a ver:\n\nEntrevista con el paciente:\n\n{phase1}\n\nDiagnositco:\n\n{phase2}\n\nSeguimiento: (cada 3 lineas es como si fuera una nueva consulta)\n\n{phase3}"

    # Generar respuesta del modelo
    chat_session = model.start_chat()
    response = chat_session.send_message(prompt)

    history = []
    history.append({"role": "user", "parts": [response.text]})

    chat_session = model.start_chat(history=history)
    evolution = chat_session.send_message("Valora la evolución del paciente con un valor del 0 al 100. Solo escribe el numero")

    return response.text, int(evolution.text)