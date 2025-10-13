from core.crew import crew

input_data = {
    'url': 'https://www.mdpi.com/2076-2607/13/9/2112',
    'raw': 'output/raw.md',
}

# Kick off the crew process
result = crew.kickoff(inputs=input_data)
print(result)