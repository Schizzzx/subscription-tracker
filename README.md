# Subscription Tracker

A simple full-stack project for tracking online subscriptions (Netflix, Spotify, YouTube, etc.).  
The backend is powered by **Django REST Framework**.  
Web and mobile clients will be added later.

---

## Current Version (v1)

This version includes:

- Project structure (backend / web / mobile)
- Django project setup (`core/`)
- `subscriptions` app with database model
- Full CRUD API (list, create, update, delete)
- Summary endpoint (`/api/summary/`) calculating:
  - monthly total
  - yearly total
  - subscription count
- Test data added via Django admin / DRF interface

Authentication is not implemented yet (`AllowAny`).

---

## Project Structure

subscription-tracker/
backend/
core/
subscriptions/
manage.py
requirements.txt
venv/ # ignored
web/ # (future React app)
mobile/ # (future React Native app)
DEVELOPER_DIARY.md
README.md
.gitignore


---

## Technologies Used

- Python  
- Django  
- Django REST Framework  
- SQLite (dev)  

Planned:
- React (web)
- React Native / Expo (mobile)
- PostgreSQL (prod)

---

## How to Run (Backend)


cd backend
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

If I didn't add the notes(Rus) to the .gitignore - there will be easier guide

## API available at:

http://127.0.0.1:8000/api/subscriptions/

http://127.0.0.1:8000/api/summary/

---

## API Endpoints
- Subscriptions
GET     /api/subscriptions/
POST    /api/subscriptions/
GET     /api/subscriptions/<id>/
PUT     /api/subscriptions/<id>/
DELETE  /api/subscriptions/<id>/

-Summary
GET /api/summary/

