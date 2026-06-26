import math
import os
import pandas as pd

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DONORS_FILE = os.path.join(_BASE, "datasets", "donors.csv")

# -------------------------
# Haversine Distance Formula
# -------------------------
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in KM
    
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return round(R * c, 2)

# -------------------------
# Blood Compatibility Chart
# -------------------------
COMPATIBLE_BLOOD_TYPES = {
    "A+": ["A+", "A-", "O+", "O-"],
    "A-": ["A-", "O-"],
    "B+": ["B+", "B-", "O+", "O-"],
    "B-": ["B-", "O-"],
    "AB+": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
    "AB-": ["A-", "B-", "AB-", "O-"],
    "O+": ["O+", "O-"],
    "O-": ["O-"]
}

# -------------------------
# Find Matching Donors
# -------------------------
def find_matching_donors(blood_group, request_latitude, request_longitude, top_n=10):
    donors_df = pd.read_csv(DONORS_FILE)
    
    # Filter by blood group compatibility, availability, and approved status
    is_avail = (donors_df["isAvailable"] == True) | (donors_df["isAvailable"].astype(str).str.lower() == "true")
    is_approved = donors_df["status"].astype(str).str.lower() == "approved"
    
    compatible_types = COMPATIBLE_BLOOD_TYPES.get(blood_group.upper(), [blood_group.upper()])
    
    donors_df = donors_df[
        donors_df["bloodGroup"].str.upper().isin(compatible_types) & is_avail & is_approved
    ]
    
    if donors_df.empty:
        return []
        
    matched_donors = []
    
    for idx, donor in donors_df.iterrows():
        distance = calculate_distance(
            request_latitude,
            request_longitude,
            donor["lat"],
            donor["lng"]
        )
        
        matched_donors.append({
            "donorId": idx,
            "name": donor["name"],
            "bloodGroup": donor["bloodGroup"],
            "phone": donor["phone"],
            "city": donor["city"],
            "distanceKm": distance
        })
        
    matched_donors.sort(key=lambda x: x["distanceKm"])
    return matched_donors[:top_n]