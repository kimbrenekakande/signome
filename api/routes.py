from fastapi import APIRouter   
router = APIRouter()

@router.get('/')
def hella():
    return{'status' : 'ok'}