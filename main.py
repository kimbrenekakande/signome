from core.crew import crew

input_data = {
    'url': 'https://bmcmicrobiol.biomedcentral.com/articles/10.1186/s12866-025-04242-7',
    'raw': 'output/raw.md',
    'image': 'https://media.springernature.com/lw685/springer-static/image/art%3A10.1186%2Fs12866-025-04242-7/MediaObjects/12866_2025_4242_Fig5_HTML.png'
}

# Kick off the crew process
result = crew.kickoff(inputs=input_data)


print(result)