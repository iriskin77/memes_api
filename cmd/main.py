from fastapi import FastAPI
from memes.api.handlers import router

app = FastAPI()

app.include_router(router)
