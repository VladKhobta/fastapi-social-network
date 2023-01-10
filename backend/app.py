from fastapi import FastAPI, Depends
from . import api

app = FastAPI()

app.include_router(api.router)
