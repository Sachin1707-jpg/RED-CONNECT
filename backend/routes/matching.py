from fastapi import APIRouter, HTTPException
import pandas as pd
import os

from services.matching_service import find_matching_donors

router = APIRouter()

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUESTS_FILE = os.path.join(_BASE, "datasets", "requests.csv")

@router.get("/match/{request_id}")
def match_donors(request_id: int):
    try:
        requests_df = pd.read_csv(REQUESTS_FILE)
        
        if request_id < 0 or request_id >= len(requests_df):
            raise HTTPException(status_code=404, detail="Blood request not found")
            
        request = requests_df.iloc[request_id]
        
        # pandas Series doesn't support .get() — use square brackets with a fallback
        blood_group = str(request["bloodGroup"])
        lat = float(request["lat"])
        lng = float(request["lng"])
        urgency = str(request["urgency"]) if "urgency" in requests_df.columns else "normal"
        status  = str(request["status"])  if "status"  in requests_df.columns else "pending"
        hospital_name = str(request["hospitalName"]) if "hospitalName" in requests_df.columns else ""
        
        matched_donors = find_matching_donors(
            blood_group=blood_group,
            request_latitude=lat,
            request_longitude=lng
        )
        
        return {
            "requestId":           request_id,
            "hospitalName":        hospital_name,
            "bloodGroup":          blood_group,
            "urgency":             urgency,
            "status":              status,
            "matchedDonorsCount":  len(matched_donors),
            "matchedDonors":       matched_donors
        }
        
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="requests.csv not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/match")
def test_matching():
    return {"message": "Matching API Working Successfully"}