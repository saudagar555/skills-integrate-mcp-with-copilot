"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

from typing import Dict, List

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    }

}

# In-memory clubs/committees database
clubs_committees: Dict[str, Dict] = {
    # Example structure
    "Science Club": {
        "description": "Explore science topics and experiments",
        "members": ["teacher@mergington.edu", "student1@mergington.edu"],
        "roles": {"teacher@mergington.edu": "advisor", "student1@mergington.edu": "member"}
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

# --- Club/Committee Endpoints ---
@app.get("/clubs_committees")
def get_clubs_committees():
    """Get all clubs and committees"""
    return clubs_committees

@app.post("/clubs_committees/{club_name}/add_member")
def add_member_to_club(club_name: str, email: str, role: str = "member"):
    """Add a member to a club/committee"""
    if club_name not in clubs_committees:
        raise HTTPException(status_code=404, detail="Club/Committee not found")
    club = clubs_committees[club_name]
    if email in club["members"]:
        raise HTTPException(status_code=400, detail="Member already exists")
    club["members"].append(email)
    club["roles"][email] = role
    return {"message": f"Added {email} as {role} to {club_name}"}

@app.delete("/clubs_committees/{club_name}/remove_member")
def remove_member_from_club(club_name: str, email: str):
    """Remove a member from a club/committee"""
    if club_name not in clubs_committees:
        raise HTTPException(status_code=404, detail="Club/Committee not found")
    club = clubs_committees[club_name]
    if email not in club["members"]:
        raise HTTPException(status_code=400, detail="Member not found")
    club["members"].remove(email)
    club["roles"].pop(email, None)
    return {"message": f"Removed {email} from {club_name}"}

@app.post("/clubs_committees/create")
def create_club_or_committee(club_name: str, description: str):
    """Create a new club or committee"""
    if club_name in clubs_committees:
        raise HTTPException(status_code=400, detail="Club/Committee already exists")
    clubs_committees[club_name] = {"description": description, "members": [], "roles": {}}
    return {"message": f"Created {club_name}"}

@app.delete("/clubs_committees/delete")
def delete_club_or_committee(club_name: str):
    """Delete a club or committee"""
    if club_name not in clubs_committees:
        raise HTTPException(status_code=404, detail="Club/Committee not found")
    clubs_committees.pop(club_name)
    return {"message": f"Deleted {club_name}"}


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
