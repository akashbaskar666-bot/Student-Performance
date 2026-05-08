import streamlit as st
import requests

st.title("🎓 Student Success Predictor")
st.write("Enter student details below to see the AI prediction.")

# Form inputs[cite: 1]
hours = st.number_input("Hours Studied", 0.0, 24.0, 5.0)
attendance = st.number_input("Attendance %", 0.0, 100.0, 80.0)
sleep = st.number_input("Sleep Hours", 0.0, 15.0, 7.0)
score = st.number_input("Previous Score", 0.0, 100.0, 60.0)

if st.button("Predict Result"):
    # Send data to FastAPI
    payload = {
        "Hours_Studied": hours,
        "Attendance": attendance,
        "Sleep_Hours": sleep,
        "Previous_Score": score
    }
    
    response = requests.post("http://127.0.0.1:8000/predict", json=payload)
    
    if response.status_code == 200:
        res = response.json()
        prediction = res["prediction"]
        
        if prediction == "Pass":
            st.success(f"The model predicts: {prediction} ✅")
        else:
            st.error(f"The model predicts: {prediction} ❌")
    else:
        st.error("Backend Error. Is FastAPI running?")