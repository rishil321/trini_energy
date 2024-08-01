from typing import List
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from fastapi_backend.models import (
    Company,
    NaturalGasProductionByCompany,
    NaturalGasUtilizationBySector,
)
from fastapi_backend.database import get_db, session

# set up environment
app = FastAPI()
load_dotenv()


@app.get("/")
def home():
    return {"message": "First FastAPI app"}


@app.get("/natural-gas/production")
def natural_gas_production(session: Session = Depends(get_db)):
    result = session.query(NaturalGasProductionByCompany).all()
    return result
