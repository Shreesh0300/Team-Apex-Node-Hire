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


class ProposalSubmission(BaseModel):
    job_id: int
    freelancer_email: str
    cover_letter: str
    bid_amount: str


class JobData(BaseModel):
    title: str
    description: str
    required_skills: str
    budget_range: str
    deadline: str
    project_type: str

@app.post("/post-job")
async def create_job(job: JobData):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = """INSERT INTO jobs 
                 (title, description, required_skills, budget_range, deadline, project_type) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        val = (job.title, job.description, job.required_skills, job.budget_range, job.deadline, job.project_type)
        cursor.execute(sql, val)
        conn.commit()
        return {"message": "Project published to the marketplace!"}
    except Exception as e:
        return {"message": f"Database Error: {str(e)}"}
    finally:
        cursor.close()
        conn.close()

@app.get("/jobs")
async def get_all_jobs():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM jobs")
        columns = [column[0] for column in cursor.description]
        jobs = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return jobs
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

@app.post("/submit-proposal")
async def submit_proposal(data: ProposalSubmission):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = """INSERT INTO proposals 
                 (job_id, freelancer_email, cover_letter, bid_amount) 
                 VALUES (%s, %s, %s, %s)"""
        val = (data.job_id, data.freelancer_email, data.cover_letter, data.bid_amount)
        cursor.execute(sql, val)
        conn.commit()
        return {"message": "Proposal submitted successfully!"}
    except Exception as e:
        return {"message": f"Database Error: {str(e)}"}
    finally:
        cursor.close()
        conn.close()
class EvaluationRequest(BaseModel):
    job_description: str
    proposal_text: str

@app.post("/evaluate")
async def evaluate_proposal(data: EvaluationRequest):
    job_words = set(data.job_description.lower().replace(',', '').split())
    proposal_words = set(data.proposal_text.lower().replace(',', '').split())
    
    matches = job_words.intersection(proposal_words)
    
    if len(job_words) == 0:
        score = 0
    else:
        base_score = int((len(matches) / len(job_words)) * 100)
        score = min(base_score + 45, 98) 
        
    if score > 85:
        feedback = f"🔥 Highly Recommended: Strong overlap in core skills. Detected key matches: {', '.join(list(matches)[:3])}."
    elif score > 60:
        feedback = f"⚠️ Moderate Match: Covers basics but might be missing specific technical requirements."
    else:
        feedback = f"❌ Low Priority: The proposal fails to address the main requirements of the job description."

    return {
        "score": score,
        "feedback": feedback
    }
@app.get("/proposals")
async def get_all_proposals():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM proposals")
        columns = [column[0] for column in cursor.description]
        proposals = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return proposals
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()