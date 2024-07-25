from dotenv import load_dotenv
from fastapi import FastAPI

# set up environment
app = FastAPI()
load_dotenv()


@app.get("/")
def home():
    return {"message": "First FastAPI app"}
