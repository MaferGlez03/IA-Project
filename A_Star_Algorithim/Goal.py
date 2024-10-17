class GoalCheck:
    @staticmethod
    def is_goal(state):
        #print(f"Checking goal: Progress = {state.progress.improvement_percentage}%, Severe Symptoms = {[s.name for s in state.symptoms if s.severity == 'severe']}")
        return (
            state.progress.improvement_percentage >= 80 or
            all(s.severity != "severe" for s in state.symptoms)
        )
