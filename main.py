from fastapi import FastAPI
from database import engine, Base
from api_trabajo import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
