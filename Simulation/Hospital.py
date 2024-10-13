import simpy

class Hospital:
    def __init__(self,env,procedures):
        self.env = env
        self.procedures = procedures
        self.doctors = {}
        self.patients = []
        self.medical_records = {}
        self.availability = 50
        self.patients_treated = 0
    
    def take_patient(self):
        patient = self.patients[0]
        self.patients.pop(0)
        return patient
        
class Procedure:
    def __init__(self, name, utilities, function, result, purpose ):
        self.name = name
        self.utilities = utilities
        self.function = function
        self. result = result
        self.availability = True
        self.price = 20
        self.uses = 0
        self.purpose=purpose
        
    def __hash__(self):
        return hash((self.name))
        
class Utility:
    def __init__(self, name, ammount):
        self.name = name
        self.ammount = ammount
        self.availability = ammount!=0
        self.status = 100

class Disease:
    def __init__(self, name, symptom, progress = 10):
        self.name = name 
        self.symptom = symptom
        self.progress = progress
        
    def __hash__(self):
        return hash((self.name))

    def __eq__(self, other):
        return isinstance(other, Disease) and self.name == other.name
        
class Symptom:
    def __init__(self, name, severity, treatments, diagnostic_tests):
        self.name = name
        self.severity = severity
        self.treatments = treatments
        self.diagnostic_tests = diagnostic_tests