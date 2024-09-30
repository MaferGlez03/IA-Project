from Support import *
class State:
    def __init__(self, medications, procedures, symptoms, progress, general_state, disease_stage=None):
        self.medications = medications
        self.procedures = procedures
        self.symptoms = symptoms
        self.progress = progress
        self.general_state = general_state
        self.disease_stage = disease_stage
        self.cost = 0
    
    def __str__(self):
        state_str = (
            f"Medications: {[str(m) for m in self.medications]}\n"
            f"Procedures: {[str(p) for p in self.procedures]}\n"
            f"Symptoms: {[str(s) for s in self.symptoms]}\n"
            f"Progress: {self.progress}\n"
            f"General State: {self.general_state}\n"
        )
        return state_str
    
    def __lt__(self, other):
        return self.cost < other.cost

    # Update methods (inside State class)
    def update_symptoms(self, action):
        new_symptoms = self.symptoms.copy()
        effects = action.effects_symptoms
        
        for symptom, effect in effects.items():
            if effect == 'reveal' and symptom not in new_symptoms:
                new_symptoms.append(Symptom(symptom, "moderate"))
            elif effect == 'alleviate':
                new_symptoms = [s for s in new_symptoms if s.name != symptom]
            elif effect == 'worsen':
                for s in new_symptoms:
                    if s.name == symptom:
                        s.severity = "severe"
        
        return new_symptoms

    def update_progress(self, action):
        new_progress = self.progress.improvement_percentage + action.effects_progress
        new_progress = max(0, min(100, new_progress))
        
        return Progress(new_progress)

    def update_general_state(self, updated_progress, updated_symptoms):
        new_energy_level = self.general_state.energy_level + (updated_progress.improvement_percentage / 10)
        new_pain_level = sum(1 for s in updated_symptoms if s.severity == "severe")
        
        new_energy_level = max(0, min(10, new_energy_level))
        new_pain_level = max(0, min(10, new_pain_level))
        
        return StateGeneral(new_energy_level, new_pain_level, self.general_state.immune_status)

