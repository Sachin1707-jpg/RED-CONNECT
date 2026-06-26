// REDCONNECT - Global Data Fetcher from FastAPI Backend

window.demoData = {
  donors: [],
  hospitals: [],
  blood_requests: []
};

window.fetchBackendData = async function() {
  try {
    const API_BASE = 'http://localhost:8000/api';
    
    // Fetch all endpoints concurrently
    const [donorsRes, hospRes, reqRes] = await Promise.all([
      fetch(`${API_BASE}/donors`),
      fetch(`${API_BASE}/hospitals`),
      fetch(`${API_BASE}/requests`)
    ]);

    const donors = await donorsRes.json();
    const hospitals = await hospRes.json();
    const requests = await reqRes.json();

    // Transform backend data format to match what frontend expects
    window.demoData.donors = donors.map(d => ({
      id: "d" + (d.donorId !== undefined ? d.donorId : Math.random()),
      name: d.name,
      blood_group: d.bloodGroup,
      city: d.city,
      lat: parseFloat(d.lat),
      lng: parseFloat(d.lng),
      available: d.isAvailable === true || String(d.isAvailable).toLowerCase() === 'true',
      last_donation: d.lastDonation || "2024-01-01",
      donations_count: d.donationsCount || 0,
      phone: d.phone
    }));

    window.demoData.hospitals = hospitals.map(h => ({
      id: "h" + (h.hospitalId !== undefined ? h.hospitalId : Math.random()),
      name: h.name,
      city: h.city,
      lat: parseFloat(h.lat),
      lng: parseFloat(h.lng),
      contact: h.phone || h.contactPhone || "N/A",
      verified: h.status && h.status.toLowerCase() === 'approved'
    }));

    window.demoData.blood_requests = requests.map(r => {
      let mappedStatus = r.status ? r.status.charAt(0).toUpperCase() + r.status.slice(1).toLowerCase() : "Pending";
      if (mappedStatus === 'Active') mappedStatus = 'Pending';

      let mappedUrgency = r.urgency ? r.urgency.charAt(0).toUpperCase() + r.urgency.slice(1).toLowerCase() : "Normal";
      if (mappedUrgency === 'Moderate') mappedUrgency = 'Normal';

      return {
        id: "r" + (r.requestId !== undefined ? r.requestId : Math.random()),
        hospital_id: r.hospitalId,
        hospital_name: r.hospitalName,
        blood_group: r.bloodGroup,
        units: r.units,
        urgency: mappedUrgency,
        status: mappedStatus,
        city: r.city,
        lat: parseFloat(r.lat),
        lng: parseFloat(r.lng),
        created_at: r.created_at || new Date().toISOString()
      };
    });

    console.log("✅ Successfully loaded real data from backend:", {
      donors: window.demoData.donors.length,
      hospitals: window.demoData.hospitals.length,
      requests: window.demoData.blood_requests.length
    });

  } catch (error) {
    console.error("❌ Failed to fetch data from backend. Is the FastAPI server running?", error);
    // If backend fails, show empty state instead of crashing
    window.demoData = { donors: [], hospitals: [], blood_requests: [] };
  }
};
