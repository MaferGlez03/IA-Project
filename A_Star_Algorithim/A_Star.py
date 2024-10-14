import heapq
from A_Star_Algorithim.States import State
from A_Star_Algorithim.Procedures import treatment_procedures,treatment_medications

class AStar:
    def __init__(self, minimal_cost_per_action=50, minimal_cost_per_treatment=100):
        self.minimal_cost_per_action = minimal_cost_per_action
        self.minimal_cost_per_treatment = minimal_cost_per_treatment
        self.possible_procedure = treatment_procedures
        self.possible_medications = treatment_medications
        self.log = ""

    # Heuristic to guide the search (Admissible)
    def heuristic(self, state):
        return self.progress_heuristic(state) + self.symptom_heuristic(state)

    def progress_heuristic(self, state):
        if state.progress.improvement_percentage < 80:
            remaining_progress = 80 - state.progress.improvement_percentage
            steps_needed = remaining_progress / 10
            return steps_needed * self.minimal_cost_per_action
        return 0

    def symptom_heuristic(self, state):
        severe_symptoms = [s for s in state.symptoms if s.severity == "severe"]
        return len(severe_symptoms) * self.minimal_cost_per_treatment

    # Calculate the actual cost of a state
    def calculate_cost(self, state):
        total_cost = 0
        for procedure in state.procedures:
            total_cost += procedure.cost
        for medication in state.medications:
            total_cost += 50 * medication.dosage
        
        if state.progress.improvement_percentage < 50:
            total_cost += (50 - state.progress.improvement_percentage) * 10
        
        severe_symptoms = [s for s in state.symptoms if s.severity == "severe"]
        total_cost += len(severe_symptoms) * 100
        
        return total_cost

   
    # A* Search Algorithm
    def a_star(self, initial_state, is_goal):
        frontier = []
        initial_state.cost = 0  # Initialize the cost of the initial state
        heapq.heappush(frontier, (0, initial_state))
        visited = set()

        while frontier:
            _, current_state = heapq.heappop(frontier)
            
            #print(f"Expanding state with progress: {current_state.progress.improvement_percentage}% and symptoms: {[s.name for s in current_state.symptoms]}")

            if current_state in visited:
                continue
            
            if is_goal(current_state):
                print("Goal state reached!")
                return current_state

            visited.add(current_state)
            successors = self.generate_successors(current_state)

            for successor in successors:
                cost_successor = self.calculate_cost(successor)
                heuristic_successor = self.heuristic(successor)
                priority = cost_successor + heuristic_successor
                successor.cost = priority  # Store the total cost in the state object

                heapq.heappush(frontier, (priority, successor))
                #print("No solution found.")

        return None  # No solution found


    # generate_successors is placed inside AStar class
    def generate_successors(self, current_state):
        successors = []

        # 1. Perform additional procedures
        for new_procedure in self.possible_procedure:
            if new_procedure not in current_state.procedures:
                updated_symptoms = current_state.update_symptoms(new_procedure)
                updated_progress = current_state.update_progress(new_procedure)
                updated_general_state = current_state.update_general_state(updated_progress, updated_symptoms)

                new_state = State(
                    medications=current_state.medications,  # Keep the same medications
                    procedures=current_state.procedures + [new_procedure],  # Add new procedure
                    symptoms=updated_symptoms,
                    progress=updated_progress,
                    general_state=updated_general_state,
                    disease_stage=current_state.disease_stage  # Optional if used
                )
                successors.append(new_state)

        

        # 2. Administer new medications
        for new_medication in self.possible_medications:
            if new_medication not in current_state.medications:
                updated_symptoms = current_state.update_symptoms(new_medication)
                updated_progress = current_state.update_progress(new_medication)
                updated_general_state = current_state.update_general_state(updated_progress, updated_symptoms)

                new_state = State(
                    medications=current_state.medications + [new_medication],  # Add new medication
                    procedures=current_state.procedures,  # Keep the same procedures
                    symptoms=updated_symptoms,
                    progress=updated_progress,
                    general_state=updated_general_state,
                    disease_stage=current_state.disease_stage  # Optional if used
                )
                medication = f"Generated successor with medication: {new_medication.name}"
                symptoms = f"Symptoms: {[s.name for s in updated_symptoms]}"
                progress = f"Progress: {updated_progress.improvement_percentage}%"
                self.log = self.log + medication + "\n" + symptoms + "\n" + progress + "\n"
                print(medication)
                print(symptoms)
                print(progress)
                successors.append(new_state)

        return successors
