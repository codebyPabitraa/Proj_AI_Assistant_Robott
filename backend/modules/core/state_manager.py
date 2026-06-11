class StateManager:

    def __init__(self):

        self.current_state = "idle"

    def set_state(self, state: str):

        self.current_state = state

    def get_state(self):

        return self.current_state