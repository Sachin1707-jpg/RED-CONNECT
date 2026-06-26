from fastapi import APIRouter, HTTPException
from services.csv_service import get_donors

router = APIRouter()

# Get all donors
@router.get("/donors")
def get_all_donors():
    df = get_donors()
    return df.to_dict(orient="records")


# Get donor by ID
@router.get("/donors/{donor_id}")
def get_donor_by_id(donor_id: int):
    df = get_donors()

    donor = df[df["donorId"] == donor_id]

    if donor.empty:
        raise HTTPException(
            status_code=404,
            detail="Donor not found"
        )

    return donor.to_dict(orient="records")[0]


# Get donors by blood group
@router.get("/donors/blood/{blood_group}")
def get_donors_by_blood_group(blood_group: str):
    df = get_donors()

    donors = df[
        df["bloodGroup"].str.upper() ==
        blood_group.upper()
    ]

    return donors.to_dict(orient="records")


# Get available donors only
@router.get("/donors/available")
def get_available_donors():
    df = get_donors()

    # Handle string boolean or actual boolean
    is_avail = (df["isAvailable"] == True) | (df["isAvailable"].astype(str).str.lower() == "true")
    
    available = df[is_avail]

    return available.to_dict(orient="records")