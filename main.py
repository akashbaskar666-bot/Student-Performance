from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import sqlite3
from datetime import datetime

app = FastAPI()
model = joblib.load("student_model.pkl")

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS predictions 
                     (id INTEGER PRIMARY KEY, timestamp TEXT, hours REAL, 
                      attendance REAL, sleep REAL, score REAL, result TEXT)''')
    conn.commit()
    conn.close()

init_db()

class StudentData(BaseModel):
    Hours_Studied: float
    Attendance: float
    Sleep_Hours: float
    Previous_Score: float

@app.post("/predict")
def get_prediction(data: StudentData):
    # 1. Prediction Logic
    features = np.array([[data.Hours_Studied, data.Attendance, data.Sleep_Hours, data.Previous_Score]])
    prediction = model.predict(features)
    result = "Pass" if prediction[0] == 1 else "Fail"
    
    # 2. Save to Database (Memory)
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO predictions (timestamp, hours, attendance, sleep, score, result) VALUES (?, ?, ?, ?, ?, ?)",
                   (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data.Hours_Studied, data.Attendance, data.Sleep_Hours, data.Previous_Score, result))
    conn.commit()
    conn.close()

    return {"prediction": result}

@app.get("/history")
def get_history():
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return {"history": rows}