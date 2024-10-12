from Simulation.Hospital import Hospital 
import random

def beliefs():
    return {
        'disease_progress': 50,  # 1-100
        'confidence_treatment': random.randint(3, 7), # all values 1-10
        'welfare_feeling': random.randint(3, 7), 
        'family_history': random.randint(3, 7), 
        'knowledge_disease': random.randint(3, 7), 
        'patient': random.randint(0, 9), 
        'has_bed': False, 
        'has_left': False
    }

def desires():
    return {
        'improve_quality_life': False,
        'avoid_side_effects': False,
        'seek_second_opinions': False,
        'explore_alternative_treatments': False,
        'reduce_impact_daily_life': False,
        'want_bed': False,
        'want_left': False
    }

def brf(perception, beliefs):
    """
    Belief-Revision Function (BRF) actualiza las creencias del agente con base en 
    la percepción del entorno y el estado actual del hospital.
    """
    # Revisar si se canso de esperar
    if 'has_left' in perception:
        beliefs['has_left'] = True

    if 'has_bed' in perception:
        beliefs['has_bed'] = True

    # Revisar la disponibilidad de cama en el hospital
    if 'patient' in perception:
        beliefs['patient'] = perception['patient']

    # Actualizar progresión de la enfermedad basada en síntomas y procedimientos
    if 'disease_progress' in perception:
        beliefs['disease_progress'] = perception['disease_progress']

    # Actualizar la confianza en el tratamiento según los procedimientos realizados
    if 'confidence_treatment' in perception:
        beliefs['confidence_treatment'] = perception['confidence_treatment']

    # Actualizar si el paciente se siente bien o mal
    if 'welfare_feeling' in perception:
        beliefs['welfare_feeling'] = perception['welfare_feeling'] 

    # Considerar historial familiar del paciente
    if 'family_history' in perception:
        beliefs['family_history'] = perception['family_history']

    # Conocimiento del paciente sobre su enfermedad
    if 'knowledge_disease' in perception:
        beliefs['knowledge_disease'] = perception['knowledge_disease']

def generate_option(beliefs, desires):
    if not beliefs['has_bed']:
        desires['want_bed'] = True

    elif beliefs['patient'] >= 10:
        desires['want_left'] = True
        
    elif beliefs['disease_progress'] > 50:
        desires['improve_quality_life'] = True

    elif beliefs['confidence_treatment'] < 5:
        desires['seek_second_opinions'] = True

    elif beliefs['welfare_feeling'] < 5:
        desires['avoid_side_effects'] = True

    elif beliefs['family_history'] > 5:
        desires['reduce_impact_daily_life'] = True

    elif beliefs['knowledge_disease'] > 5:
        desires['explore_alternative_treatments'] = True

def filter(beliefs, desires):
    """
    Filtra los deseos que no sean relevantes o posibles en base a las creencias del paciente.
    """
    # Deseo de obtener una cama si no tiene
    if not beliefs['has_bed']:
        desires['want_bed'] = True
    else:
        desires['want_bed'] = False

    # Si la progresión de la enfermedad es avanzada, desea mejorar la calidad de vida
    if beliefs['disease_progress'] > 70:
        desires['improve_quality_life'] = True
    else:
        desires['improve_quality_life'] = False

    # Si la confianza en el tratamiento es baja, desea buscar segundas opiniones
    if beliefs['confidence_treatment'] < 4:
        desires['seek_second_opinions'] = True
    else:
        desires['seek_second_opinions'] = False

    # Si el paciente se siente bien, prefiere evitar efectos secundarios
    if beliefs['welfare_feeling'] < 5:
        desires['avoid_side_effects'] = True
    else:
        desires['avoid_side_effects'] = False

    # Si tiene historial familiar de la enfermedad, desea reducir su impacto en la vida diaria
    if beliefs['family_history'] > 5:
        desires['reduce_impact_daily_life'] = True
    else:
        desires['reduce_impact_daily_life'] = False

    # Si tiene buen conocimiento sobre la enfermedad, podría explorar tratamientos alternativos
    if beliefs['knowledge_disease'] > 5:
        desires['explore_alternative_treatments'] = True
    else:
        desires['explore_alternative_treatments'] = False

def execute_action(hospital, beliefs, desires, perception, results, env, patient):
    """
    Ejecuta las acciones de acuerdo con las intenciones formadas.
    """
    if desires['want_left']:
        print("Se canso de esperar")
        perception['has_left'] = True
        yield env.timeout(2)
        return

    # if beliefs['has_bed']:
    #     perception['has_bed'] = True
    #     yield env.timeout(2)
    #     return

    elif desires['want_bed']:
        # Buscar cama disponible en el hospital
        if hospital.availability:
            print("Asignando cama al paciente...")
            results.append((env.now,f"A bed has been assigned to patiend {patient.name}"))
            perception['has_bed'] = True
            hospital.availability -= 1
            yield env.timeout(2)
            return
        else:
            print("No hay camas disponibles en este momento.")
            results.append((env.now,f"Hospital is full. There is no bed availabilty for {patient.name}"))
            perception['patient'] = beliefs['patient'] + 1
            yield env.timeout(5)

    if desires['improve_quality_life']:
        # Ejecutar procedimientos para mejorar la calidad de vida
        for procedure in hospital.procedures:
            if procedure.function == "improve quality life" and procedure.availability:
                print(f"Aplicando procedimiento: {procedure.name}")
                results.append((env.now,f"Apply procedure: {procedure.name} to patient {patient.name}"))
                perception['welfare_feeling'] = beliefs['welfare_feeling'] + 1
                yield env.timeout(2)
                return

    if desires['seek_second_opinions']:
        # Consultar con otro doctor
        print("Buscando una segunda opinión médica...")
        results.append((env.now,f"Patient {patient.name} is lookin up for another doctor opinion"))
        perception['confidence_treatment'] = beliefs['confidence_treatment'] - 1
        perception['knowledge_disease'] = beliefs['knowledge_disease'] + 1
        yield env.timeout(2)
        return

    if desires['avoid_side_effects']:
        # Evitar tratamientos agresivos
        print("Evitando tratamientos con altos efectos secundarios...")
        results.append((env.now,f"Patient {patient.name} prefer to avoid secondary effects"))
        perception['welfare_feeling'] = beliefs['welfare_feeling'] - 1
        yield env.timeout(2)
        return

    if desires['reduce_impact_daily_life']:
        # Aplicar estrategias para reducir el impacto de la enfermedad en la vida diaria
        print("Implementando estrategias para reducir el impacto en la vida diaria...")
        results.append((env.now,f"Patient {patient.name} will implement strategies to reduce impact on daily life "))
        perception['family_history'] = beliefs['family_history'] - 1
        yield env.timeout(2)
        return

    if desires['explore_alternative_treatments']:
        # Explorar tratamientos alternativos
        print("Explorando tratamientos alternativos...")
        results.append((env.now,f"Patient {patient.name} is looking up for alternative treatments "))
        perception['knowledge_disease'] = beliefs['knowledge_disease'] - 1
        perception['confidence_treatment'] = beliefs['confidence_treatment'] + 1
        perception['family_history'] = beliefs['family_history']+ 1
        yield env.timeout(2)
        return


