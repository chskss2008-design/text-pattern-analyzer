from dfa import TextDFA

machine = TextDFA()

result = machine.process(["W", "W", "E"])

print("Input: W W E")
print("Final State:", result["final_state"])
print("Accepted:", result["accepted"])
print("State History:", result["history"])
