from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="nodehire_db"
    )

class User(BaseModel):
    name: str
    email: str
    password_hash: str
    role: str
    bio: str = ""
    hourly_rate: float = 0.0

@app.get("/users")
def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

@app.post("/register")
def register_user(user: User):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO Users (name, email, password_hash, role, bio, hourly_rate) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (user.name, user.email, user.password_hash, user.role, user.bio, user.hourly_rate)
    try:
        cursor.execute(query, values)
        conn.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        cursor.close()
        conn.close()
    return {"message": "User registered successfully"}
class ProposalData(BaseModel):
    job_description: str
    proposal_text: str

@app.post("/evaluate")
async def evaluate_proposal(data: ProposalData):
    score = 0
    feedback = ""
    
    proposal_lower = data.proposal_text.lower()
    job_lower = data.job_description.lower()

    if len(proposal_lower) > 50:
        score += 30
    else:
        feedback += "Proposal lacks detail. "

    words = job_lower.split()
    match_count = sum(1 for word in words if len(word) > 3 and word in proposal_lower)
    
    if match_count > 0:
        score += 50
        feedback += f"Strong keyword alignment ({match_count} matches). "
    else:
        feedback += "Missing core requirements. "
        
    score = min(score + 15, 98) 

    if score > 80:
        feedback += "Highly recommended candidate."
    elif score > 50:
        feedback += "Potential fit, requires interview."

    return {"score": score, "feedback": feedback.strip()}