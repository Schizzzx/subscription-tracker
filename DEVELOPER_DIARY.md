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
  - `billing_period` (`monthly`, `yearly`, `weekly`)
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
- Added initial test data.
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
- Applied global `IsAuthenticated`.
- Enforced strict user data isolation:
  - `get_queryset()` filters only the current user’s data.
  - `perform_create()` automatically assigns `user=request.user`.
  - Declared `user` field as read-only in serializers.
- Protected `/api/summary/` with authentication.
- Fully tested JWT + Session login + isolation behavior.

**Backend now has robust authentication and strict per-user data separation.**

---

## Day 3 — Trials, Notifications, Friends, and Common Subscriptions

### ✔ Trials System Implemented

Added trial-related fields to `Subscription`:
- `has_trial`
- `trial_end_date`
- `auto_renews`

Updated Summary API:
- Excludes subscriptions still in trial.

Tested:
- Trial fields save correctly.
- Summary logic behaves as expected.

---

### ✔ Notification Settings (Initial Version)

Model:
- `days_before`
- `email_enabled`
- `push_enabled`
- One-to-One with `User`

Endpoint:
- `/api/notification-settings/`

Tested basic creation and isolation.

---

### ✔ Friends System Implemented

Model:
- `from_user`
- `to_user`
- `status` (`pending`, `accepted`, `rejected`)
- `created_at`

Features:
- Users can send friend requests.
- Requests visible to both sides.
- Accept/decline via PATCH.

Endpoints:
- `/api/friends/`
- `/api/friends/<id>/`

---

### ✔ Common Subscriptions Feature

Endpoint:
- `/api/common/`

Logic:
- Works only when friendship is accepted.
- Case-insensitive subscription name matching.
- Returns suggestions for shared/family plans.

Tested and verified.

---

## Day 4 — Data Integrity, Ownership Hardening & Notification Settings Upsert

### ✔ 1. Unique Subscriptions Per User

- Added database-level `UniqueConstraint(user, name)` in the `Subscription` model.
- Cleaned legacy duplicate rows in SQLite before migration.
- Implemented duplicate detection in the `SubscriptionSerializer`:
  - User-friendly 400 error before DB-level constraint triggers.
- Added `perform_update()` in `SubscriptionViewSet` to enforce:
  - `user=request.user` on all updates.

### ✔ 2. Ownership Protection Improvements

- Both `Subscription` and `NotificationSettings` explicitly prevent any user tampering via API payload.
- User assignment is enforced exclusively through backend logic.

### ✔ 3. Notification Settings — Upsert Behavior

**New behavior:**

- `POST /api/notification-settings/` now acts as **UPSERT**:
  - If user has no settings → create.
  - If settings exist → update them (200 OK).
- Makes frontend integration significantly simpler (no need for conditional logic).

### ✔ 4. Cleanup & Stability

- Removed duplicate `Subscription` rows before applying constraints.
- Verified that:
  - Duplicate subscriptions cannot be created.
  - Notification settings remain single-per-user.
  - Users cannot change ownership on any resource.

---

## ✔ Current Backend Status (Stable v1)

- JWT authentication  
- Session authentication  
- Per-user data isolation  
- Subscription CRUD  
- Subscription uniqueness enforcement  
- Trial system  
- Summary totals  
- Notification settings (with upsert)  
- Friends system  
- Common subscriptions detection  
- Ownership protection for all models

Backend is now stable, consistent, and ready for frontend integration.

---

## TODO — Future Development Roadmap

### Backend Improvements
- Pagination for subscription and friend list endpoints.
- Celery-based notification scheduler (email + push reminders).
- Service categories.
- Service logos (icons for Netflix, Spotify, YouTube, etc.).
- Audit log for subscription changes.
- Soft deletion for subscriptions (optional).

### Nice-to-Have Features
- Import subscriptions from Google Play / App Store.
- OCR for bank statements.
- CSV export.
- Cost forecasting.
- Dark/light mode for web & mobile.

---

## Notes
я ненавижу сведбанк!

