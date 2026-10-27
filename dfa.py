
class TextDFA:
    def __init__(self, pattern_type="sentence"):
        self.pattern_type = pattern_type

        if pattern_type == "sentence":
            # DFA with 2 states:
            # q0 = input does not end with punctuation
            # q1 = input ends with punctuation
            self.states = ["q0", "q1"]
            self.start_state = "q0"
            self.final_states = {"q1"}

            self.transitions = {
                "q0": {"W": "q0", "E": "q1"},
                "q1": {"W": "q0", "E": "q1"}
            }

        elif pattern_type == "word":
            # DFA with 3 states:
            # q0 = no character processed
            # q1 = a letter has been read
            # q2 = a word-ending space has been read
            self.states = ["q0", "q1", "q2"]
            self.start_state = "q0"
            self.final_states = {"q1", "q2"}

            self.transitions = {
                "q0": {"L": "q1", "S": "q0", "O": "q0"},
                "q1": {"L": "q1", "S": "q2", "O": "q0"},
                "q2": {"L": "q1", "S": "q2", "O": "q0"}
            }

        self.state = self.start_state

    def process(self, symbols):
        self.state = self.start_state
        history = []

        for position, symbol in enumerate(symbols, start=1):
            from_state = self.state
            self.state = self.transitions[self.state][symbol]

            history.append({
                "position": position,
                "symbol": symbol,
                "from_state": from_state,
                "to_state": self.state
            })

        return {
            "states": self.states,
            "final_state": self.state,
            "accepted": self.state in self.final_states,
            "history": history
        }
