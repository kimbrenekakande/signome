from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def hella():
    return[{'name' : 'tako mbeki'},{'age' : 'N/A'}]


@router.get('/zit')
def hella(sev):
    return[{'name' : 'jombi'},{'age' : sev}]

