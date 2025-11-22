from pathlib import Path
import json

def converter(state):
    
    know = Path('core')
    study = Path('core/study.md')
    
    for file in know.iterdir():
        if file.suffix == '.json':
            with open(file, 'r') as f:
                data = json.load(f)
                with open(study, 'a') as md:
                    md.write('## Image Description Data' + '\n\n')
                    for item in data:
                        img_desc = item['desc']
                        md.write(img_desc + '\n\n')
            print(file.name)
            
        else:
            pass #yet to be implement other file formats
        
    return state
