from A_Star import *
from Support import *
from Goal import *


class Main:
    @staticmethod
    def run():
        # Define the list of possible procedures
        possible_procedures = [
            Procedure(
                name="MRI Scan", 
                cost=500, 
                effects_progress=-5,  
                effects_symptoms={"Atrophy": "reveal"}  
            ),
            Procedure(
                name="Blood Test", 
                cost=100, 
                effects_progress=0, 
                effects_symptoms={"B12 Deficiency": "reveal"}  
            )
        ]


        # Define the list of possible medications
        possible_medications = [
            Medication(
                name="Painkiller", 
                dosage=1, 
                duration=7, 
                effects_progress=10,  
                effects_symptoms={"headache": "alleviate"}  
            ),
            Medication(
                name="Vitamin B12", 
                dosage=1, 
                duration=30, 
                effects_progress=30,  
                effects_symptoms={"fatigue": "alleviate"}  
            )
        ]       


        # Initialize the AStar object with the possible procedures and medications
        astar = AStar(possible_procedures, possible_medications)

        # Create an initial state for the patient
        initial_state = State(
            medications=[],  
            procedures=[],  
            symptoms=[Symptom("headache", "severe"), Symptom("fatigue", "severe")],  # Severe headache and fatigue
            progress=Progress(30),  # The patient starts with 30% progress
            general_state=StateGeneral(energy_level=3, pain_level=8, immune_status="weak")  # Poor general state
        )


        # Run the A* search algorithm
        solution = astar.a_star(initial_state, GoalCheck.is_goal)

        # Print the result
        if solution:
            print("Goal state reached:")
            print(solution)
        else:
            print("No solution found.")


# To run the program, simply call the main method
if __name__ == "__main__":
    Main.run()
