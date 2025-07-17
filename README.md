#  NeuroTutor — Personalized AI Study Guide Generator

NeuroTutor is an AI-powered web application that generates tailored study guides based on uploaded **PDFs or text files on any topic**. It uses the Gemini 1.5 Pro model to extract key topics, summaries, and potential questions, making learning and revision faster and more effective.

---

## 📸 Screenshots

### 🔹 Home Page
![Home Page Screenshot](assets/home.png)

### 🔹 Study Guide Page
![Study Page Screenshot](assets/study.png)

---

## 🚀 Features

- 📄 Upload study materials (PDFs or text)
- 🧠 Automatically generates concise study guides
- 💡 Extracts key topics and potential questions
- 🔒 JWT-based authentication with secure cookie storage
- 🌐 Fully responsive and modern UI

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask)
- **Database:** PostgreSQL (via SQLAlchemy)
- **AI Model:** Google Gemini 1.5 Pro (via API)
- **Deployment:** Render
- **Authentication:** JWT with Flask-JWT-Extended

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/neurotutor.git
cd neurotutor
2️⃣ Set up a Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
3️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Set Up Environment Variables
Create a .env file in the root directory:

ini
Copy
Edit
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_flask_secret
JWT_SECRET_KEY=your_jwt_secret
DATABASE_URL=your_postgres_connection_uri
Example DATABASE_URL format for PostgreSQL:

bash
Copy
Edit
postgresql://username:password@hostname:port/database_name
5️⃣ Run the Application
bash
Copy
Edit
python app.py
Visit the app at: http://localhost:5000