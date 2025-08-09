import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load your trained model and label encoders
model = joblib.load("car_price_model.pkl")
le_dict = joblib.load("label_encoders.pkl")

app = FastAPI()


origins = [
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],     
    allow_headers=["*"],
    allow_credentials=True,
)

class CarInfo(BaseModel):
    year: int
    odometer: float
    manufacturer: str
    model: str
    condition: str
    cylinders: str
    fuel: str
    title_status: str
    transmission: str
    drive: str
    size: str
    type: str
    paint_color: str

@app.post("/predict")
def predict(car: CarInfo):
    df = pd.DataFrame([car.dict()])

    
    for col in df.select_dtypes(include=np.number).columns:
        df[col] = df[col].fillna(df[col].median())
    for col in df.select_dtypes(include=object).columns:
        df[col] = df[col].fillna('missing')

  
    for col in df.select_dtypes(include=object).columns:
        le = le_dict[col]
       
        df[col] = df[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
        df[col] = le.transform(df[col])

    prediction = model.predict(df)[0]

    return {"predicted_price_dollar": float(prediction)}
