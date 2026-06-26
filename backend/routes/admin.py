from fastapi import APIRouter
import pandas as pd
import os

router = APIRouter()

# Resolve paths relative to THIS file so the server works regardless of CWD
_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DONORS_FILE    = os.path.join(_BASE, "datasets", "donors.csv")
HOSPITALS_FILE = os.path.join(_BASE, "datasets", "hospitals.csv")
NGOS_FILE      = os.path.join(_BASE, "datasets", "ngos.csv")
REQUESTS_FILE  = os.path.join(_BASE, "datasets", "requests.csv")


# -------------------------
# Admin Dashboard
# -------------------------
@router.get("/admin/dashboard")
def admin_dashboard():

    donors_df    = pd.read_csv(DONORS_FILE)
    hospitals_df = pd.read_csv(HOSPITALS_FILE)
    ngos_df      = pd.read_csv(NGOS_FILE)
    requests_df  = pd.read_csv(REQUESTS_FILE)

    total_donors    = len(donors_df)
    total_hospitals = len(hospitals_df)
    total_ngos      = len(ngos_df)
    total_requests  = len(requests_df)

    # donors.csv uses "isAvailable" (not "availability")
    is_avail = (
        (donors_df["isAvailable"] == True) |
        (donors_df["isAvailable"].astype(str).str.lower() == "true")
    )
    available_donors = int(is_avail.sum())

    # requests.csv uses "urgency" (not "priority")
    critical_cases = int(
        len(requests_df[requests_df["urgency"].str.lower() == "critical"])
        if "urgency" in requests_df.columns else 0
    )

    pending_requests = int(
        len(requests_df[requests_df["status"].str.lower() == "active"])
        if "status" in requests_df.columns else 0
    )

    completed_requests = int(
        len(requests_df[requests_df["status"].str.lower() == "fulfilled"])
        if "status" in requests_df.columns else 0
    )

    return {
        "totalDonors":        total_donors,
        "availableDonors":    available_donors,
        "totalHospitals":     total_hospitals,
        "totalNGOs":          total_ngos,
        "totalRequests":      total_requests,
        "criticalCases":      critical_cases,
        "pendingRequests":    pending_requests,
        "completedRequests":  completed_requests
    }


# -------------------------
# System Analytics
# -------------------------
@router.get("/admin/analytics")
def analytics():

    donors_df   = pd.read_csv(DONORS_FILE)
    requests_df = pd.read_csv(REQUESTS_FILE)

    blood_group_counts = (
        donors_df["bloodGroup"]
        .value_counts()
        .to_dict()
    )

    request_status_counts = (
        requests_df["status"]
        .value_counts()
        .to_dict()
    )

    return {
        "bloodGroupDistribution":   blood_group_counts,
        "requestStatusDistribution": request_status_counts
    }


# -------------------------
# Recent Blood Requests
# -------------------------
@router.get("/admin/recent-requests")
def recent_requests():

    requests_df = pd.read_csv(REQUESTS_FILE)

    # requests.csv has no "requestId" column — use the row index instead
    requests_df = requests_df.reset_index(drop=True)
    requests_df["requestId"] = requests_df.index

    requests_df = requests_df.sort_values(
        by="requestId",
        ascending=False
    )

    recent = requests_df.head(10)

    return recent.to_dict(orient="records")


# -------------------------
# Available Donors
# -------------------------
@router.get("/admin/available-donors")
def available_donors():

    donors_df = pd.read_csv(DONORS_FILE)

    # donors.csv uses "isAvailable" (not "availability")
    is_avail = (
        (donors_df["isAvailable"] == True) |
        (donors_df["isAvailable"].astype(str).str.lower() == "true")
    )
    donors = donors_df[is_avail]

    return donors.to_dict(orient="records")