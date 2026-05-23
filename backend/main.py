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
        password="",
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