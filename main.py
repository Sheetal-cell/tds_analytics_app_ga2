from fastapi import FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from collections import defaultdict

app = FastAPI()

# Enable CORS for all origins so the browser can verify it directly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "ak_vaoojdm5yfm2ijojlqg1i8c3"
USER_EMAIL = "25f1001114@ds.study.iitm.ac.in"  # Replace with your actual registered email address

class Event(BaseModel):
    user: str
    amount: float
    ts: int

class AnalyticsRequest(BaseModel):
    events: List[Event]

@app.post("/analytics")
def analyze_events(req: AnalyticsRequest, x_api_key: Optional[str] = Header(None)):
    # 1. Authenticate via X-API-Key header
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    
    events = req.events
    total_events = len(events)
    
    unique_users_set = set()
    user_positive_totals = defaultdict(float)
    revenue = 0.0

    for e in events:
        unique_users_set.add(e.user)
        if e.amount > 0:
            revenue += e.amount
            user_positive_totals[e.user] += e.amount

    unique_users = len(unique_users_set)

    # Find top user by highest positive-amount total
    top_user = ""
    if user_positive_totals:
        top_user = max(user_positive_totals, key=user_positive_totals.get)
    elif events:
        top_user = events[0].user

    return {
        "email": USER_EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user
    }