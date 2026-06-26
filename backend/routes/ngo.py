from fastapi import APIRouter, HTTPException
from services.csv_service import get_ngos
import pandas as pd

router = APIRouter()


# Get active NGOs  ← MUST be before /{ngo_id} to avoid route conflict
@router.get("/ngos/active")
def get_active_ngos():

    df = get_ngos()

    active_ngos = df[
        df["status"].str.lower() == "active"
    ]

    return active_ngos.to_dict(orient="records")


# Get NGOs by city  ← MUST be before /{ngo_id}
@router.get("/ngos/city/{city}")
def get_ngos_by_city(city: str):

    df = get_ngos()

    ngos = df[
        df["city"].str.lower() == city.lower()
    ]

    return ngos.to_dict(orient="records")


# Get all NGOs
@router.get("/ngos")
def get_all_ngos():

    df = get_ngos()

    # Add a synthetic ngoId based on row index (the CSV has no ngoId column)
    df = df.reset_index(drop=True)
    df["ngoId"] = df.index

    return df.to_dict(orient="records")


# Get NGO by ID (index-based, since CSV has no ngoId column)
@router.get("/ngos/{ngo_id}")
def get_ngo_by_id(ngo_id: int):

    df = get_ngos()
    df = df.reset_index(drop=True)
    df["ngoId"] = df.index

    if ngo_id < 0 or ngo_id >= len(df):
        raise HTTPException(
            status_code=404,
            detail="NGO not found"
        )

    return df.iloc[ngo_id].to_dict()