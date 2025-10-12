from core.crew import crew

input_data = {
    'file': 'input/study.pdf'
}

# Kick off the crew process
result = crew.kickoff(inputs=input_data)
print(result)