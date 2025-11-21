from fastapi import FastAPI
from api.study.routing import router as new_router


app = FastAPI()
app.include_router(new_router, prefix="/api/study")

@app.get('/')
def hella():
    return[{'name' : 'alifonso dumbe'},{'age' : '26'}]

