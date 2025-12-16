from backend.agent.phase_10_2.decomposer import MultiIntentDecomposer

decomposer = MultiIntentDecomposer()
test_clauses = [
    'Change header to green',
    'Change header text to green',
    'Make header green',
    'invalid nonsense'
]

for clause in test_clauses:
    intent = decomposer._detect_intent(clause)
    print(f'Clause: "{clause}" -> Intent: {intent}')
