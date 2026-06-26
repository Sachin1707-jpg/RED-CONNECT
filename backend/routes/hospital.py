from fastapi import APIRouter, HTTPException
from services.csv_service import get_hospitals
import pandas as pd

router = APIRouter()


# Get verified hospitals  ← MUST be before /{hospital_id} to avoid route conflict
@router.get("/hospitals/verified")
def get_verified_hospitals():
    df = get_hospitals()

    hospitals = df[
        df["status"].str.lower() == "approved"
    ]

    return hospitals.to_dict(orient="records")


# Get hospitals by city  ← MUST be before /{hospital_id}
@router.get("/hospitals/city/{city}")
def get_hospitals_by_city(city: str):

    df = get_hospitals()

    hospitals = df[
        df["city"].str.lower() == city.lower()
    ]

    return hospitals.to_dict(orient="records")


# Get all hospitals
@router.get("/hospitals")
def get_all_hospitals():

    df = get_hospitals()

    # Add a synthetic hospitalId based on row index (the CSV has no hospitalId column)
    df = df.reset_index(drop=True)
    df["hospitalId"] = df.index

    return df.to_dict(orient="records")


# Get hospital by ID (index-based, since CSV has no hospitalId column)
@router.get("/hospitals/{hospital_id}")
def get_hospital_by_id(hospital_id: int):

    df = get_hospitals()
    df = df.reset_index(drop=True)
    df["hospitalId"] = df.index

    if hospital_id < 0 or hospital_id >= len(df):
        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )

    return df.iloc[hospital_id].to_dict()