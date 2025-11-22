from fastapi import FastAPI
from api.routes import router as new_router


app = FastAPI()
app.include_router(new_router, prefix="/api")
