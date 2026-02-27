import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder


# ==========================
# TRAINING DATA
# ==========================

ages = [18, 19, 20, 21, 22, 23, 24, 25, 26]
courses = [
    "AI",
    "AI",
    "Web Development",
    "AI",
    "Data Science",
    "Web Development",
    "Data Science",
    "AI",
    "Web Development"
]

recommendations = [
    "Machine Learning",
    "Machine Learning",
    "React",
    "Deep Learning",
    "Big Data",
    "Node.js",
    "Data Engineering",
    "Computer Vision",
    "Full Stack Development"
]


# ==========================
# ENCODERS
# ==========================

course_encoder = LabelEncoder()
recommend_encoder = LabelEncoder()

encoded_courses = course_encoder.fit_transform(courses)
encoded_recommend = recommend_encoder.fit_transform(recommendations)

X = np.array(list(zip(ages, encoded_courses)))
y = encoded_recommend


# ==========================
# TRAIN MODEL
# ==========================

model = DecisionTreeClassifier()
model.fit(X, y)


# ==========================
# SAFE PREDICTION FUNCTION
# ==========================

def predict_recommendation(age: int, current_course: str):

    if not current_course:
        return "Python Programming"

    # Normalize input
    current_course = current_course.strip()

    try:
        encoded_course = course_encoder.transform([current_course])[0]
        prediction = model.predict([[age, encoded_course]])
        recommended_course = recommend_encoder.inverse_transform(prediction)[0]
        return recommended_course

    except Exception:
        # If unseen course → fallback
        return "Python Programming"