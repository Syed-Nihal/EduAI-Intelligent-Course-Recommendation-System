# 🎓 Student Intelligent Course Recommendation System

## 🚀 Overview
This project is an AI-powered backend system that recommends suitable courses for students based on their academic performance and interest level.

It combines **Machine Learning + Rule-Based Logic + Secure APIs** to deliver accurate and explainable recommendations.

---

## 🛠️ Tech Stack
- Python
- FastAPI
- SQLite
- Scikit-learn (Decision Tree)
- JWT Authentication

---

## ✨ Features
- 🔐 User Authentication (Signup/Login using JWT)
- 📊 Add & View Student Data
- 🤖 AI-Based Course Recommendation
- 🧠 Explainable AI (Reason + Confidence)
- 🔒 Protected API Endpoints
- ⚡ Fast and lightweight backend

---

## 🤖 AI Logic
- Uses **Decision Tree Classifier**
- Enhanced with **Rule-Based Logic** for better accuracy
- Provides:
  - Recommended Course
  - Reason for recommendation
  - Confidence level

---

## 📌 API Endpoints

### 🔐 Authentication
- `POST /auth/signup`
- `POST /auth/login`

### 🎓 Students
- `GET /students/all`
- `POST /students/add`
- `POST /students/recommend`

---

## 🧪 Example Request

```json
{
  "age": 22,
  "attendance": 95,
  "marks": 90,
  "interest_level": 5
}