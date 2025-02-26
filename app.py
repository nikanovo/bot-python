from fastapi import FastAPI
from webhook import webhook_app

app = FastAPI()
app.mount("/", webhook_app) 