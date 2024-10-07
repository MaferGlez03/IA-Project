class Symptom:
    def __init__(self, id, name, description, associated_diseases, treatments, diagnostic_tests):
        self.id = id
        self.name = name
        self.description = description
        self.associated_diseases = associated_diseases
        self.treatments = treatments
        self.diagnostic_tests = diagnostic_tests

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

# Example usage
if __name__ == "__main__":
    # Create some symptoms
    memory_loss = Symptom("s1", "Memory Loss", "A decline in the ability to remember information.",
                          ["Alzheimer's", "Lewy body dementia", "Huntington's"],
                          ["Cognitive therapy", "Cholinesterase inhibitors"],
                          ["Cognitive assessments", "Neuroimaging"])

    tremor = Symptom("s4", "Tremor", "Rhythmic shaking of a part of the body.",
                     ["Parkinson's", "Essential tremor"],
                     ["Medications like beta-blockers", "Surgery for severe cases"],
                     ["Neurological examination", "Blood tests to rule out other causes"])

    # Create a patient
    patient = Patient("John Doe", 65, "Male")
    
    # Add symptoms to the patient
    patient.add_symptom(memory_loss)
    patient.add_symptom(tremor)

    # Print patient information
    print(patient)
