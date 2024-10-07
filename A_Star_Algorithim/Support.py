# Symptom Class
class Symptom:
    def __init__(self, name, severity):
        self.name = name  
        self.severity = severity  # Severity (mild, moderate, severe)
    
    def __str__(self):
        return f"{self.name} (Severity: {self.severity})"


# Medication Class
class Medication:
    def __init__(self, name, dosage, duration, effects_progress=0, effects_symptoms=None):
        self.name = name
        self.dosage = dosage
        self.duration = duration
        self.effects_progress = effects_progress  # Effect on progress
        self.effects_symptoms = effects_symptoms or {}  # Effect on symptoms
    
    def __str__(self):
        return f"{self.name} (Dosage: {self.dosage}, Duration: {self.duration})"


# Procedure Class
class Procedure:
    def __init__(self, name, cost, effects_progress=0, effects_symptoms=None, result=None):
        self.name = name
        self.cost = cost
        self.effects_progress = effects_progress  # Effect on progress
        self.effects_symptoms = effects_symptoms or {}  # Effect on symptoms
        self.result = result
    
    def __str__(self):
        return f"{self.name} (Cost: {self.cost}, Result: {self.result})"


# Progress Class
class Progress:
    def __init__(self, improvement_percentage):
        self.improvement_percentage = improvement_percentage  # 0-100%
    
    def __str__(self):
        return f"Progress: {self.improvement_percentage}%"

    
# StateGeneral Class
class StateGeneral:
    def __init__(self, energy_level, pain_level, immune_status):
        self.energy_level = energy_level  # 0 - 10
        self.pain_level = pain_level  # 0 - 10
        self.immune_status = immune_status  # weak, normal, compromised, severe
    
    def __str__(self):
        return f"Energy: {self.energy_level}, Pain: {self.pain_level}/10, Immune Status: {self.immune_status}"
