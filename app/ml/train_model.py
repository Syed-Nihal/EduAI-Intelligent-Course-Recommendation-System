import sqlite3
import os
import joblib
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# =========================
# Database & Model Path
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, "students.db")
MODEL_PATH = os.path.join(BASE_DIR, "ml", "student_model.pkl")


def train_and_save_model():

    # Connect to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Using 4 features
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

    # Features (4 columns)
    X = data[:, 0:4]

    # Target
    y = data[:, 4]

    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    print("\n========== TRAINING MODELS ==========\n")

    # Decision Tree
    dt_model = DecisionTreeClassifier(random_state=42)
    dt_model.fit(X_train, y_train)
    dt_predictions = dt_model.predict(X_test)
    dt_acc = accuracy_score(y_test, dt_predictions)

    print("Decision Tree Accuracy:", dt_acc)
    print("Decision Tree Report:\n", classification_report(y_test, dt_predictions))

    # Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_predictions = rf_model.predict(X_test)
    rf_acc = accuracy_score(y_test, rf_predictions)

    print("\nRandom Forest Accuracy:", rf_acc)
    print("Random Forest Report:\n", classification_report(y_test, rf_predictions))

    # Choose best model
    if rf_acc >= dt_acc:
        best_model = rf_model
        print("\n✅ Random Forest selected as final model")
    else:
        best_model = dt_model
        print("\n✅ Decision Tree selected as final model")

    # Save model
    joblib.dump(best_model, MODEL_PATH)

    print("\n🎉 Model trained and saved successfully!")
    print("📁 Saved at:", MODEL_PATH)


if __name__ == "__main__":
    train_and_save_model()