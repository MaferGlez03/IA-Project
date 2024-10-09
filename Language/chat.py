import os
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
    model = configure_model(f"{role}, you are in a neurodegenerative disease center and I need you to determine in 5 interactions what disease the patient may have. In order to record the symptoms, I need you to invite the patient to mention the symptom explicitly. Only spanish")

    history = []

    # Iniciar la conversación
    print("Antes de iniciar rellena el siguiente cuestionario")

    name = input("Nombre completo: ")
    age = input("Edad (en números): ")
    sex = input("Sexo M o F: ")
    print()
    if sex == "M" or "m": sex = "Male"
    else: sex = "Female"

    # Crear un paciente
    patient = Patient(name, age, sex)

    print("Doctor: Buenas en qué te puedo ayudar hoy?")

    while True:
        user_input = input("You: ")

        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(user_input)

        # Identificar síntomas en el texto del paciente
        symptoms_found = identify_symptoms(user_input)

        # Añadir los síntomas identificados al paciente
        for symptom in symptoms_found:
            patient.add_symptom(symptom)

        # Mostrar respuesta del modelo
        print(f"Doctor: {response.text}")
        print()

        # Almacenar la historia de la conversación
        history.append({"role": "user", "parts": [user_input]})
        history.append({"role": "model", "parts": [response.text]})

        # Finalizar si el paciente termina la conversación
        if "adios" in user_input.lower():
            break

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

    return response.text