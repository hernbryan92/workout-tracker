# workout-tracker
Full-stack workout tracking web application built with Flask. Users can log workouts, track progress, and manage training history with authentication and database persistence.

## 🚀 Features
- User authentication (Register / Login / Logout)
- Per-user workout tracking
- Add and delete workouts
- Stats dashboard with:
  - Total workouts
  - Unique exercises
  - Most common exercise
  - Personal records (max weight)
  - Workouts in the last 7 days
- Clean, responsive UI with Bootstrap

## 🛠️ Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite, SQLAlchemy
- **Authentication:** Flask-Login
- **Frontend:** HTML, Jinja2, Bootstrap 5
- **Version Control:** Git & GitHub

## 📸 Screenshots
*(Add screenshots here later)*

## ⚙️ Installation & Setup
```bash
git clone https://github.com/hernbryan92/workout-tracker.git
cd workout-tracker
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python run.py