from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import os

router = APIRouter()

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUESTS_FILE = os.path.join(_BASE, "datasets", "requests.csv")

# -------------------------
# Pydantic Models
# -------------------------
class BloodRequest(BaseModel):
    patientName: str
    bloodGroup: str
    units: int
    urgency: str
    hospitalName: str
    hospitalId: str
    city: str
    contactPhone: str
    status: str
    lat: float
    lng: float

class StatusUpdate(BaseModel):
    status: str

# -------------------------
# Get All Requests
# -------------------------
@router.get("/requests")
def get_all_requests():
    df = pd.read_csv(REQUESTS_FILE)
    # Add id column based on index
    df["requestId"] = df.index
    return df.to_dict(orient="records")

# -------------------------
# Dashboard Statistics  ← MUST be before /{request_id} to avoid route conflict
# -------------------------
@router.get("/requests/stats")
def request_statistics():
    df = pd.read_csv(REQUESTS_FILE)

    total_requests     = len(df)
    critical_cases     = len(df[df["urgency"].str.lower() == "critical"]) if "urgency" in df.columns else 0
    pending_requests   = len(df[df["status"].str.lower() == "active"])   if "status"  in df.columns else 0
    completed_requests = len(df[df["status"].str.lower() == "fulfilled"]) if "status"  in df.columns else 0

    return {
        "totalRequests":     total_requests,
        "criticalCases":     critical_cases,
        "pendingRequests":   pending_requests,
        "completedRequests": completed_requests
    }

# -------------------------
# Get Request By ID
# -------------------------
@router.get("/requests/{request_id}")
def get_request_by_id(request_id: int):
    df = pd.read_csv(REQUESTS_FILE)
    if request_id < 0 or request_id >= len(df):
        raise HTTPException(status_code=404, detail="Request not found")

    request = df.iloc[request_id].to_dict()
    request["requestId"] = request_id
    return request

# -------------------------
# Create New Request
# -------------------------
@router.post("/requests")
def create_request(request: BloodRequest):
    df = pd.read_csv(REQUESTS_FILE)

    new_row = request.model_dump() if hasattr(request, "model_dump") else request.dict()
    new_row["verified"] = False

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(REQUESTS_FILE, index=False)

    return {
        "message": "Blood request created successfully",
        "requestId": len(df) - 1
    }

# -------------------------
# Update Request Status
# -------------------------
@router.patch("/requests/{request_id}")
def update_request_status(request_id: int, payload: StatusUpdate):
    df = pd.read_csv(REQUESTS_FILE)
    if request_id < 0 or request_id >= len(df):
        raise HTTPException(status_code=404, detail="Request not found")

    df.loc[request_id, "status"] = payload.status
    df.to_csv(REQUESTS_FILE, index=False)
    return {"message": "Status updated successfully"}

# -------------------------
# Delete Request
# -------------------------
@router.delete("/requests/{request_id}")
def delete_request(request_id: int):
    df = pd.read_csv(REQUESTS_FILE)
    if request_id < 0 or request_id >= len(df):
        raise HTTPException(status_code=404, detail="Request not found")

    df = df.drop(request_id)
    df.to_csv(REQUESTS_FILE, index=False)
    return {"message": "Request deleted successfully"}