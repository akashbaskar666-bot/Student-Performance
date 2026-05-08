import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. Load your dataset
# For this example, we assume a CSV with: Hours_Studied, Attendance, Sleep_Hours, Previous_Score, Result
df = pd.read_csv("student_performance.csv") 

# 2. Basic Cleaning & Encoding
# Convert 'Pass' to 1 and 'Fail' to 0
df['Result'] = df['Result'].map({'Pass': 1, 'Fail': 0})

# 3. Define Features (X) and Target (y)
X = df[['Hours_Studied', 'Attendance', 'Sleep_Hours', 'Previous_Score']]
y = df['Result']

# 4. Split and Train[cite: 1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# 5. Export the "Brain"
joblib.dump(model, "student_model.pkl")
print("Model saved as student_model.pkl")