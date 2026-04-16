import pandas as pd
from sklearn.tree import DecisionTreeClassifier


# ==============================
# 🎯 TRAIN MODEL (IMPROVED)
# ==============================
def train_model():
    data = {
        "age": [18,19,20,21,22,23,24,25],
        "attendance": [90,85,70,60,95,50,80,75],
        "marks": [85,80,65,50,90,40,78,72],
        "interest_level": [5,4,3,2,5,1,4,3],
        "course": [
            "AI/ML",
            "Data Science",
            "Web Development",
            "Basic IT",
            "AI/ML",
            "Basic IT",
            "Data Science",
            "Web Development"
        ]
    }

    df = pd.DataFrame(data)

    X = df[["age","attendance","marks","interest_level"]]
    y = df["course"]

    model = DecisionTreeClassifier()
    model.fit(X, y)

    return model


# ==============================
# 🔮 PREDICT COURSE (SMART LOGIC)
# ==============================
def predict_course(model, student_data: dict):
    
    # 🔥 RULE-BASED BOOST (VERY IMPORTANT)
    if student_data["marks"] > 85 and student_data["interest_level"] >= 4:
        return "AI/ML"

    if student_data["marks"] > 75 and student_data["attendance"] > 80:
        return "Data Science"

    if student_data["interest_level"] >= 3:
        return "Web Development"

    # fallback ML
    input_data = pd.DataFrame([student_data])
    prediction = model.predict(input_data)

    return prediction[0]