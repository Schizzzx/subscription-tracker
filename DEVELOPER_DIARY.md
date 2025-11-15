# Developer Diary — Subscription Tracker

A structured development log documenting the backend and API progress of the Subscription Tracker project.

---

## Day 1 — Backend Initialization

### ✔ Done

- Created project structure:
  - `backend/`
  - `web/`
  - `mobile/`
- Added `.gitignore` and initialized GitHub repository.
- Created and activated virtual environment (`venv/`).
- Installed dependencies:
  - **Django**
  - **Django REST Framework**
  - **psycopg2-binary**
- Created Django project: `core/`.
- Created application: `subscriptions/`.
- Implemented base `Subscription` model:
  - `user` (FK)
  - `name`, `price`, `currency`
  - `billing_period` (monthly / yearly / weekly)
  - `next_payment_date`
  - `is_active`
- Implemented CRUD API using DRF `ModelViewSet`.
- Implemented `SubscriptionSerializer`.
- Added `/api/subscriptions/` endpoint via DRF router.
- Added `/api/summary/` endpoint with:
  - monthly total
  - yearly total
  - subscription count
- Created admin test user:
  - username: `admin`
  - password: `cocacola`
- Added initial test data (Netflix subscriptions).
- First GitHub push completed.

---

## Day 2 — Authentication, Permissions and User Isolation

### ✔ Done

- Installed **djangorestframework-simplejwt**.
- Added authentication endpoints:
  - `/api/token/`
  - `/api/token/refresh/`
- Configured REST Framework to use:
  - `JWTAuthentication`
  - `SessionAuthentication`
- Enabled browser login via `/api-auth/login/`.
- Applied global `IsAuthenticated` permission.
- Implemented strict user data isolation:
  - `get_queryset()` filters by current user.
  - `perform_create()` assigns `user=request.user`.
  - `user` field set to read-only.
- Protected summary API (`/api/summary/`).
- Successfully tested:
  - JWT authentication
  - Session login
  - Proper 401 responses
  - User-specific subscription listing
  - User-specific summary totals

**Backend now has proper authentication and isolation.**

---

## Day 3 — Trials, Notifications, Friends, and Common Subscriptions

### ✔ 1. Trials System Implemented

New fields in subscription model:
- `has_trial`
- `trial_end_date`
- `auto_renews`

Summary now excludes subscriptions still in trial.

Tested:
- Trial field saves correctly
- Summary ignores trial subscriptions
- Normal subscriptions counted as expected

---

### ✔ 2. Notification Settings Added

New model:  
- `days_before`
- `email_enabled`
- `push_enabled`
- Auto-bound to current user

Endpoint:
- `/api/notification-settings/`

Tested:
- Settings create and save properly
- Bound to user
- Appears in DRF UI

---

### ✔ 3. Friends System Implemented

New model:
- `from_user`
- `to_user`
- `status` (`pending`, `accepted`, `declined`)
- `created_at`

Features:
- Users can send friend requests
- Both sides see the request
- Requests can be accepted/declined via PATCH

Endpoints:
- `/api/friends/`
- `/api/friends/<id>/`

Tested:
- Sending request ✔  
- Accepting request ✔  
- Status updates ✔  

---

### ✔ 4. Common Subscriptions Feature

Endpoint:
- `/api/common/`

Logic:
- Only works if friendship = `accepted`
- Compares active subscriptions
- Case-insensitive service matching
- Returns suggestions (e.g. share plan to save money)

Tested:
- Works when both users have matching subscriptions
- Empty array if no matches or no accepted friendship

---

## ✔ Current Backend Status

Everything below is **implemented and working:**

- JWT authentication  
- Session authentication  
- User isolation  
- Subscription CRUD  
- Summary totals  
- Trial system  
- Notification settings  
- Friends system  
- Common subscription detection  

The backend is now structurally solid and ready for further expansion or frontend integration.

---

## TODO — Future Development Roadmap

###  Backend Improvements

- Prevent duplicate subscription entries for same service per user.
- Prevent users from setting others as subscription owners.
- Prevent duplicate notification settings.
- Add Celery-based notification scheduler (emails + push).
- Add pagination.
- Add service categories (optional).
- Add service logos (Netflix, Spotify, YouTube, etc.).
- Add audit log (history of changes).

---

###  Nice-to-Have Features

- Import subscriptions from Google Play / App Store.
- OCR for bank statements.
- CSV export.
- Cost forecasting.
- Web & mobile themes (dark/light mode).

---

## Notes

пока все(

---

