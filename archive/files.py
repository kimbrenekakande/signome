from ntpath import isfile
import json, os
from pathlib import Path

from browser_use.utils import P

folder = Path('media/')




def get_names():
    for file in folder.iterdir(): #iterdir interates the directory
        if file :
            # file.rename('getto.py')
            #is_file, is_dir, file.name, glob(*.py) file.suffix
            # with file.open('a') as f:
            #     f.write('FUCKKKKKKKKKK')
            print(file.name)
get_names()


fuck = Path('media/images.json')
if fuck.exists():
    print('___________')
    print('fuckery')