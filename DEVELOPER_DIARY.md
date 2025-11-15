# Developer Diary — Subscription Tracker

A short development log documenting the progress of the project.

---

## Day 1 — Backend Initialization

### Done:

- Created project structure:
  - `backend/`
  - `web/`
  - `mobile/`
- Added `.gitignore` and initial repository setup.
- Created virtual environment (`venv/`).
- Installed dependencies:
  - Django
  - Django REST Framework
  - psycopg2-binary
- Created Django project (`core/`).
- Created app `subscriptions/`.
- Added `Subscription` model:
  - user (FK)
  - name, price, currency
  - billing_period (monthly/yearly/weekly)
  - next_payment_date
  - is_active
- Applied migrations.
- Implemented CRUD API using DRF (`SubscriptionViewSet`).
- Added `SubscriptionSerializer`.
- Added `/api/subscriptions/` endpoint via DRF router.
- Added summary endpoint (`/api/summary/`) returning:
  - monthly total
  - yearly total
  - subscription count
- Created test user:
  - username: `admin`
  - password: `cocacola`
- Added first test subscriptions (two Netflix entries).
- Pushed first version to GitHub.

---

## Next Steps

- Add user authentication (token/JWT).
- Restrict API so each user sees only their own subscriptions.
- Add filters and sorting (price, active, next payment date).
- Begin React web client.
- Begin mobile app (Expo/React Native).