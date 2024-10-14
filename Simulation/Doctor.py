from Simulation import Hospital

def beliefs(symptoms, knowledge_model):
    # Initialize a dictionary to store beliefs
    beliefs_dict = {}
    
    # Get the diagnosis from the knowledge model (returns a dictionary with disease probabilities)
    diagnosis = knowledge_model.predict_disease([s.name for s in symptoms])
    
    if diagnosis:
        # Add diseases with high probability to beliefs (threshold can be adjusted)
        beliefs_dict = {disease: prob for disease, prob in diagnosis.items() if prob > 15}
        
    
    # Return the dictionary of beliefs
    return beliefs_dict


def brf(beliefs, new_symptoms, knowledge_model):
    # Check the diagnosis from the knowledge model for new symptoms
    new_diagnosis = knowledge_model.predict_disease([s.name for s in new_symptoms])
    
    if new_diagnosis:
        # Update beliefs with new information
        for disease, prob in new_diagnosis.items():
            
            if disease in beliefs:
                # If disease already exists, update its probability
                beliefs[disease] = max(beliefs[disease], prob)  # Take the higher probability
            else:
                if prob > 15:
                # If new disease is discovered, add to beliefs
                    beliefs[disease] = prob
                
    # Example logic to hypothesize a new disease if current beliefs do not match
    if not beliefs:
        # If there are no beliefs, form a new one based on severity of symptoms
        beliefs.append(form_new_belief(new_symptoms))

    return beliefs

def form_new_belief(symptoms):
    # Hypothesize a new disease based on symptoms
    new_disease_name = f"Unknown Disease {len(symptoms)}"
    return {Hospital.Disease(new_disease_name, symptoms): 100}  # Assign 100% to the unknown disease


def desires(beliefs, threshold):
    desires_dict = {}

    # Generate desires based on the beliefs
    for disease, prob in beliefs.items():
            desires_dict[disease]={}
            desires_dict[disease]["investigate_symptoms"] =  False
            desires_dict[disease]["reduce_symptoms"] =  (False,[])
            desires_dict[disease]["prevent_progression"] =  False
            desires_dict[disease]["discharge_patient"] = disease.progress <= threshold
        
    return desires_dict



#! FIX IT BY TAKING IN ACCOUNT THE PROGRESS OF THE DISEASE
def filter(beliefs, desires, patient, priority_threshold=40, progression_threshold=50):
    # Initialize a list to store filtered intentions
    intentions = []
    count =0 
    for disease, desire_actions in desires.items():
        if desire_actions.get(f"discharge_patient",False):
            count +=1
    if count == len(beliefs):
        intentions.append((f'Patient {patient.name} can be discharged',''))
        return intentions
    # Generate intentions based on desires, beliefs, and disease-specific progression
    for disease, desire_actions in desires.items():
        prob = beliefs[disease]  # Accede a la probabilidad de la enfermedad
        progression = disease.progress  # Accede al progreso de la enfermedad
        
         # Verificar si hay que reducir síntomas o prevenir progresión
        if desire_actions['reduce_symptoms'][0]==True:
            intentions.append((f"Apply treatments to reduce symptoms of {disease.name}", desire_actions['reduce_symptoms'][1]))
            return intentions
        
        # Priorizar acciones basadas en probabilidad o progreso de la enfermedad
        if prob < priority_threshold or progression < progression_threshold:
            # Verificar si hay que investigar síntomas
            if desire_actions.get("investigate_symptoms", False):
                intentions.append((f"Investigate symptoms for {disease.name}",''))
                return intentions


        if desire_actions.get("prevent_progression", False):
            intentions.append((f"Implement strategies to prevent progression of {disease.name}",''))
            return intentions

# Return the list of filtered intentions
    return intentions




def generate_options(beliefs, symptoms, procedures, desires_dict):
    # Actualizamos el diccionario existente de deseos
    for disease, prob in beliefs.items():
        if prob >= 20:  # Consider only significant beliefs
            # Si la enfermedad ya existe en desires_dict, seguimos trabajando con ella
            if disease not in desires_dict:
                desires_dict[disease] = {}

            # Obtener los síntomas relacionados con la enfermedad
            if symptoms:
                related_symptoms = [symptom for symptom in symptoms if symptom.name in disease.symptom]
                if len(related_symptoms) == 0 and len(symptoms) != 0:
                    related_symptoms = symptoms
                for symptom in related_symptoms:
                    # Verificar procedimientos disponibles para el síntoma
                    available_procedures = [proc for proc in procedures if ((proc.name.lower() in [s.lower() for s in symptom.treatments]) and (proc.availability))] #!!!!!CHECK

                    # Generar deseos basados en los procedimientos disponibles
                    if available_procedures:
                        desires_dict[disease]["reduce_symptoms"] = (True,related_symptoms)
                if not related_symptoms:   
                    desires_dict[disease]["investigate_symptoms"] = True
            else:
                desires_dict[disease]["discharge_patient"] = True
        else:
            # Si la creencia es débil, centrarse en la prevención
            desires_dict[disease] = {
                "prevent_progression": True
            }

    # Retornar el diccionario de deseos actualizado
    return desires_dict



def execute_action(intentions, patient, procedures,results,env,desires,beliefs):
    # Execute each intention
    for intention in intentions:
        if "can be discharged" in intention[0]:
            results.append((env.now,f"Patient {patient.name} has been discharged"))

        elif "Investigate symptoms" in intention[0]:
            disease = ' '.join(intention[0].split()[-2:] ) # Extract disease name from intention
            for procedure in procedures: 
                if procedure.purpose == 'treatment': #!AQUI VA DIAGNOSIS
                    result = f"Used {procedure.name} to investigate new symptoms for {disease} in {patient.name}"
                    procedure.uses += 1
                    results.append((env.now,result))
                    # Simular el descubrimiento de nuevos síntomas
                    new_symptom = f"New symptom for {disease}" #!Aqui arreglar con los results del procedure
                    #patient.symptoms.append(new_symptom)
                    d = take_disease(disease, beliefs)
                    desires[d]["investigate_symptoms"] =  False
                    yield env.timeout(10)

        elif "Apply treatments to reduce symptoms" in intention[0]:
            disease = ' '.join(intention[0].split()[-2:] )  # Extract disease name from intention
            # Encontrar un procedimiento coincidente para esta enfermedad
            #! Aqui el A_Star
            for procedure in procedures:
                if len(intention[1]):
                    disease_symptoms=intention[1]
                    if procedure.name.lower() in (t.lower() for t in disease_symptoms[0].treatments) and procedure.availability:
                        # Reducir la severidad solo si el resultado del procedimiento es bueno
                        if procedure.result == "good":
                            result = f"Applied {procedure.name} successfully to reduce symptoms of {disease} in {patient.name}"
                            procedure.uses += 1
                            results.append((env.now,result))
                            # Reducir la severidad del síntoma
                            if len(disease_symptoms) == 0:
                                patient.disease_progress = 0
                                continue
                            if disease_symptoms[0] not in patient.symptoms:
                                while disease_symptoms[0] not in patient.symptoms:
                                    disease_symptoms.remove(disease_symptoms[0])
                                    if len(disease_symptoms) == 0:
                                        break
                                if len(disease_symptoms) == 0:
                                    patient.disease_progress = 0
                                    continue
                            if len(patient.symptoms) == 0:
                                d = take_disease(disease, beliefs)
                                desires[d]["reduce_symptoms"] = False
                                # yield env.timeout(10)
                                continue
                            elif len(patient.symptoms) == 1:
                                patient.symptoms = []
                            else:
                                patient.symptoms = [symptom for symptom in patient.symptoms if symptom.name != disease_symptoms[0].name]
                                cured_symptom=disease_symptoms[0].name
                                disease_symptoms = [symptom for symptom in disease_symptoms if symptom.name != cured_symptom]
                            d = take_disease(disease, beliefs)
                            d.progress -= d.progress / (len(patient.symptoms) + 1) #!Parche 
                            patient.disease_progress = d.progress
                            desires[d]["reduce_symptoms"] = False
                            yield env.timeout(10)
                        else:
                            result = f"{procedure.name} applied, but the result was not effective for {disease} in {patient.name}"
                            results.append((env.now,result))
                            procedure.uses += 1
                            yield env.timeout(10)

        elif "prevent progression" in intention[0]:
            disease = ' '.join(intention[0].split()[-2:] ) # Extract disease name from intention
            result = f"Implemented monitoring plan for {disease} in {patient.name}"
            results.append((env.now,result))
            d = take_disease(disease, beliefs)
            desires[d]["prevent progression"] =  False
            # Reducir la progresión de la enfermedad
            yield env.timeout(10)

    
def take_disease(disease, beliefs):
    diseases = list(beliefs.keys())
    for dis in diseases:
        if dis.name.lower() == disease.lower():
            return dis
    