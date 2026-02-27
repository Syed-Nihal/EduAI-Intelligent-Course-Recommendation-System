import sqlite3
import os
import joblib
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


DATABASE = "students.db"

# Dynamically get correct model save path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "student_model.pkl")


def train_and_save_model():

    # Connect to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # 🔥 Now using 4 features
    cursor.execute("""
        SELECT age, attendance, marks, interest_level, recommended_course
        FROM students
    """)

    rows = cursor.fetchall()
    conn.close()

    if len(rows) < 5:
        print("❌ Not enough data to train model. Add more students.")
        return

    data = np.array(rows)

    # Features (first 4 columns)
    X = data[:, :-1]

    # Target (last column)
    y = data[:, -1]

    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    print("\n========== TRAINING MODELS ==========\n")

    # ===============================
    # 1️⃣ Decision Tree
    # ===============================
    dt_model = DecisionTreeClassifier(random_state=42)
    dt_model.fit(X_train, y_train)

    dt_predictions = dt_model.predict(X_test)

    print("Decision Tree Accuracy:", accuracy_score(y_test, dt_predictions))
    print("Decision Tree Report:\n", classification_report(y_test, dt_predictions))

    # ===============================
    # 2️⃣ Random Forest
    # ===============================
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    rf_predictions = rf_model.predict(X_test)

    print("\nRandom Forest Accuracy:", accuracy_score(y_test, rf_predictions))
    print("Random Forest Report:\n", classification_report(y_test, rf_predictions))

    # ===============================
    # Save the better model
    # ===============================
    dt_acc = accuracy_score(y_test, dt_predictions)
    rf_acc = accuracy_score(y_test, rf_predictions)

    if rf_acc >= dt_acc:
        best_model = rf_model
        print("\n✅ Random Forest selected as final model")
    else:
        best_model = dt_model
        print("\n✅ Decision Tree selected as final model")

    joblib.dump(best_model, MODEL_PATH)

    print("\n🎉 Model trained and saved successfully!")
    print("📁 Saved at:", MODEL_PATH)


if __name__ == "__main__":
    train_and_save_model()