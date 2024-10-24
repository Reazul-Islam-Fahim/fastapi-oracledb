from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def hi():
    return {"hello" : "world"}