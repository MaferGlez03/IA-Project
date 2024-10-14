import json
from Simulation import Hospital

class Symptom:
    def __init__(self, id, name, description, associated_diseases, treatments, diagnostic_tests):
        self.id = id
        self.name = name
        self.description = description
        self.associated_diseases = associated_diseases
        self.treatments = treatments
        self.diagnostic_tests = diagnostic_tests
        
    def __hash__(self):
        return hash((self.name))

    def __eq__(self, other):
        return isinstance(other, Symptom) and self.name == other.name

class Disease:
    def __init__(self, id, name, description, symptoms, treatments, diagnostic_tests, risk_factors):
        self.id = id
        self.name = name
        self.description = description
        self.symptoms = symptoms
        self.treatments = treatments
        self.diagnostic_tests = diagnostic_tests
        self.risk_factors = risk_factors
        
    

class Treatments:
    def __init__(self) -> None:
        pass

class Patient:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        self.disease_progress = 50
        self.symptoms = []
        self.diseases = {}
        self.treatments = []
        self.diagnostic_tests_results = {}
        self.energy_level=0
        self.pain_level=0

    def add_symptom(self, symptom):
        with open("Knowledge/ontology.json", 'r') as file:
            ontology = json.load(file)
        symptom_name = symptom.name
        if symptom_name not in [s.name for s in self.symptoms]:
            symp = Hospital.Symptom(symptom_name, "severe", [ontology_symptom['treatments'] for ontology_symptom in ontology['symptoms'] if ontology_symptom['name'] == symptom_name][0], [ontology_symptom['diagnostic_tests'] for ontology_symptom in ontology['symptoms'] if ontology_symptom['name'] == symptom_name][0])
            self.symptoms.append(symp)

    def add_disease(self, disease):
        self.diseases.append(disease)

    def set_disease_progress(self, number):
        self.disease_progress = number

    def record_diagnostic_test_result(self, test_name, result):
        self.diagnostic_tests_results[test_name] = result

    def __str__(self):
        return (f"Patient Name: {self.name}\n" 
                f"Age: {self.age}\n"
                f"Gender: {self.gender}\n"
                f"Symptoms: {[s.name for s in self.symptoms]}\n")

