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
        self.symptoms = []
        self.diseases = []
        self.treatments = []
        self.diagnostic_tests_results = {}

    def add_symptom(self, symptom):
        if symptom not in self.symptoms:
            self.symptoms.append(symptom)

    def add_disease(self, disease):
        self.diseases.append(disease)

    def record_diagnostic_test_result(self, test_name, result):
        self.diagnostic_tests_results[test_name] = result

    def __str__(self):
        return (f"Patient Name: {self.name}\n" 
                f"Age: {self.age}\n"
                f"Gender: {self.gender}\n"
                f"Symptoms: {[s.name for s in self.symptoms]}\n"
                f"Diseases: {[d.name for d in self.diseases]}\n"
                f"Treatments: {[t.name for t in self.treatments]}\n")

