from pathlib import Path
import os, json

def converter():
        know = Path('knowledge')
        folder = Path('knowledge/images.json')
        study = Path('knowledge/study.md')
        
        for file in know.iterdir():
            if file.suffix == '.md':
                print(file.name)
        #convert all files in knowledge folder to md and append to study.md
        # if folder.exists():
        #     with open(folder, 'r') as f:
        #         data = json.load(f)
        #         with open(study, 'a') as md:
        #             md.write('## Image Description Data' + '\n\n')
        #             for item in data:
        #                 img_desc = item['desc']
        #                 md.write(img_desc + '\n\n')
        # else:
        #     print('No images found')       
converter()