import simpy

class Hospital:
    def __init__(self,env,procedures):
        self.env = env
        self.procedures = procedures
        self.doctors= {}
        self.patients = {}
        self.medical_records ={}
        self.availability=[]
        
class Procedure:
    def __init__(self, name, utilities, function, result, price = 20):
        self.name= name
        self.utilities = utilities
        self.function = function
        self. result = result
        self.availability = True
        self.price = price
        self.uses = 0
        
class Utility:
    def __init__(self, name, ammount):
        self.name = name
        self.ammount = ammount
        self.availability = True
        self.status = 100

class Disease:
    def __init__(self, name, symptom, progress = 10):
        self.name = name 
        self.symptom = symptom
        self.progress = progress
        
class Symptom:
    def __init__(self, name, severity, treatments, diagnostic_tests):
        self.name= name
        self.severity = severity
        self. tratments = treatments
        self.diagnostic_tests = diagnostic_tests