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


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


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


# In-memory club/member database
clubs = {
    "Chess Club": {
        "description": "Competitive chess practice and tournaments",
        "members": ["michael@mergington.edu", "daniel@mergington.edu"],
        "status": "active"
    }
}

members = {
    "michael@mergington.edu": {
        "name": "Michael",
        "email": "michael@mergington.edu",
        "joined_clubs": ["Chess Club"]
    },
    "daniel@mergington.edu": {
        "name": "Daniel",
        "email": "daniel@mergington.edu",
        "joined_clubs": ["Chess Club"]
    }
}


@app.get("/clubs")
def get_clubs():
    return clubs


@app.post("/clubs")
def create_club(name: str, description: str):
    if name in clubs:
        raise HTTPException(status_code=400, detail="Club already exists")
    clubs[name] = {
        "description": description,
        "members": [],
        "status": "active"
    }
    return {"message": f"Club '{name}' created"}


@app.get("/clubs/{club_name}")
def get_club(club_name: str):
    if club_name not in clubs:
        raise HTTPException(status_code=404, detail="Club not found")
    return clubs[club_name]


@app.patch("/clubs/{club_name}")
def update_club(club_name: str, description: str = None, status: str = None):
    if club_name not in clubs:
        raise HTTPException(status_code=404, detail="Club not found")

    if description:
        clubs[club_name]["description"] = description
    if status:
        clubs[club_name]["status"] = status

    return {"message": f"Club '{club_name}' updated"}


@app.post("/clubs/{club_name}/members")
def add_member_to_club(club_name: str, email: str, name: str = None):
    if club_name not in clubs:
        raise HTTPException(status_code=404, detail="Club not found")

    if email in clubs[club_name]["members"]:
        raise HTTPException(status_code=400, detail="Member already in club")

    clubs[club_name]["members"].append(email)
    if email not in members:
        members[email] = {"name": name or email.split("@")[0], "email": email, "joined_clubs": []}

    members[email]["joined_clubs"].append(club_name)
    return {"message": f"Added member '{email}' to club '{club_name}'"}


@app.delete("/clubs/{club_name}/members/{member_email}")
def remove_member_from_club(club_name: str, member_email: str):
    if club_name not in clubs:
        raise HTTPException(status_code=404, detail="Club not found")

    if member_email not in clubs[club_name]["members"]:
        raise HTTPException(status_code=400, detail="Member not in club")

    clubs[club_name]["members"].remove(member_email)
    if member_email in members:
        members[member_email]["joined_clubs"].remove(club_name)

    return {"message": f"Removed member '{member_email}' from club '{club_name}'"}


@app.get("/members")
def get_members():
    return members


@app.get("/members/{email}")
def get_member(email: str):
    if email not in members:
        raise HTTPException(status_code=404, detail="Member not found")
    return members[email]
