from typing import List, Dict
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from pip._internal.utils import datetime
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, JSONResponse, HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

#a
@app.get("/ping")

def ping():
    return Response(content="PONG" , media_type="text/plain" , status_code=200)

#b

class Characteristics(BaseModel):
    max_speed: float
    max_fuel_capacity: float

class Car(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristics: Characteristics


cars_db: Dict[str, Car] = {}

@app.post("/cars", status_code=201)
def create_car(car: Car):
    if car.identifier in cars_db:
        raise HTTPException(status_code=400, detail="Car already exists")
    cars_db[car.identifier] = car
    return {"message": "Car created successfully", "car": car}

# c
@app.get("/cars", response_model=List[Car])
def get_cars():
    return list(cars_db.values())


#d
@app.get("/cars/{id}", response_model=Car)
def get_car(id: str):
    if id not in cars_db:
        raise HTTPException(status_code=404, detail=f"Car with id {id} not found")
    return cars_db[id]


#e
@app.put("/cars/{id}/characteristics", response_model=Car)
def update_characteristics(id: str, new_characteristics: Characteristics):
    if id not in cars_db:
        raise HTTPException(status_code=404, detail=f"Car with id {id} not found")

    car = cars_db[id]
    car.characteristics = new_characteristics
    cars_db[id] = car
    return car








