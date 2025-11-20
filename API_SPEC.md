# API Specification — Subscription Tracker (v1)

All endpoints require **authentication**.  
Supported authentication methods:

- **JWT** (`/api/token/`, `/api/token/refresh/`)
- **Django Session Auth** (via `/api-auth/login/` for the browsable DRF interface)

Base development URL:  
`http://localhost:8000/`

---

# 1. Authentication

## 1.1. POST `/api/token/`

Obtain a new JWT **access** and **refresh** token pair.

### Request

{
  "username": "admin",
  "password": "cocacola"
}

### Response (200)

{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}

---

## 1.2. POST `/api/token/refresh/`

Exchange a **refresh token** for a new access token.

### Request

{
  "refresh": "<refresh_token>"
}

### Response (200)

{
  "access": "<new_access_token>"
}

---

## 1.3. Session Authentication (browsable API)

* Login: `/api-auth/login/`
* Logout: `/api-auth/logout/`

You can browse all DRF endpoints via the browser UI when authenticated with a Django session.

---

# 2. Global API Behavior

## 2.1. Authentication & Permissions

Defined in `REST_FRAMEWORK` settings:

* `DEFAULT_AUTHENTICATION_CLASSES`:

  * `SessionAuthentication`
  * `JWTAuthentication`
* `DEFAULT_PERMISSION_CLASSES`:

  * `IsAuthenticated`

**All endpoints in this document require authentication.**

---

## 2.2. Pagination

Global DRF pagination:

* `DEFAULT_PAGINATION_CLASS = PageNumberPagination`
* `PAGE_SIZE = 10`

### Standard List Response Format

{
  "count": 23,
  "next": "http://localhost:8000/api/subscriptions/?page=2",
  "previous": null,
  "results": [
    { "... first page objects ..." }
  ]
}

Pagination applies to:

* `GET /api/subscriptions/`
* `GET /api/friends/`
* `GET /api/notification-settings/` (usually 0–1 object)

---

# 3. Subscriptions

## Subscription Model

{
  "id": 1,
  "user": 1,
  "name": "Netflix",
  "price": "9.99",
  "currency": "EUR",
  "billing_period": "monthly",      // "monthly" | "yearly" | "weekly"
  "next_payment_date": "2025-01-01",
  "is_active": true,

  "has_trial": false,
  "trial_end_date": null,
  "auto_renews": true
}

### Business Rules

* `user` is **read-only** and always set to the authenticated user.
* `(user, name)` is **unique** (database constraint + serializer validation).
* Name comparison during validation is **case-insensitive**.

---

## 3.1. GET `/api/subscriptions/`

Return a paginated list of all subscriptions owned by the current user.

### Query Params

* `page` — optional page number

### Example Response (200)

{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 1,
      "name": "Netflix",
      "price": "9.99",
      "currency": "EUR",
      "billing_period": "monthly",
      "next_payment_date": "2025-01-01",
      "is_active": true,
      "has_trial": false,
      "trial_end_date": null,
      "auto_renews": true
    },
    {
      "id": 2,
      "user": 1,
      "name": "Spotify",
      "price": "4.99",
      "currency": "EUR",
      "billing_period": "monthly",
      "next_payment_date": "2025-01-10",
      "is_active": true,
      "has_trial": true,
      "trial_end_date": "2025-02-01",
      "auto_renews": true
    }
  ]
}

---

## 3.2. POST `/api/subscriptions/`

Create a new subscription for the authenticated user.

### Request Body

{
  "name": "Netflix",
  "price": "9.99",
  "currency": "EUR",
  "billing_period": "monthly",
  "next_payment_date": "2025-01-01",
  "is_active": true,
  "has_trial": false,
  "trial_end_date": null,
  "auto_renews": true
}

### Notes

* `user` is ignored if provided.
* Duplicate names for the same user are rejected.

### Example Error (400)

{
  "name": ["You already have a subscription with this name."]
}

---

## 3.3. GET `/api/subscriptions/{id}/`

Return a specific subscription.

* Only available if the subscription’s `user` matches `request.user`.
* Otherwise: **404 Not Found** (hidden for security).

---

## 3.4. PUT/PATCH `/api/subscriptions/{id}/`

Update subscription fields.

### Rules

* `user` cannot be changed.
* Backend enforces `user = request.user` during updates.

### Example PATCH Request

{
  "price": "12.99",
  "is_active": false
}

### Example Response

{
  "id": 1,
  "user": 1,
  "name": "Netflix",
  "price": "12.99",
  "currency": "EUR",
  "billing_period": "monthly",
  "next_payment_date": "2025-01-01",
  "is_active": false,
  "has_trial": false,
  "trial_end_date": null,
  "auto_renews": true
}

---

## 3.5. DELETE `/api/subscriptions/{id}/`

Hard-delete the subscription.

---

# 4. Summary

## 4.1. GET `/api/summary/`

Return aggregated cost metrics for the current user.

### Summary Logic

A subscription is **excluded** from totals if:

* `has_trial == true`
* AND `trial_end_date != null`
* AND `trial_end_date` is **today or later** (trial still active)

### Example Response

{
  "monthly_total": 29.97,
  "yearly_total": 359.64,
  "count": 3
}

Fields:

* `monthly_total` — monthly spending (yearly/weekly normalized)
* `yearly_total` — yearly spending
* `count` — number of active subscriptions (not necessarily included in totals due to trials)

---

# 5. Notification Settings

## NotificationSettings Model

{
  "id": 1,
  "user": 1,
  "days_before": 3,
  "email_enabled": true,
  "push_enabled": false
}

### Rules

* One-to-One with `User`: each user has **at most one** record.
* `user` is always read-only and equals the authenticated user.

---

## 5.1. GET `/api/notification-settings/`

Paginated list of the current user’s notification settings (0 or 1 object).

### Example Response

{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 1,
      "days_before": 3,
      "email_enabled": true,
      "push_enabled": false
    }
  ]
}

If none exist:

{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}

---

## 5.2. POST `/api/notification-settings/` (UPSERT)

Upsert logic:

* If no settings exist → **create** (201).
* If settings exist → **update and return** (200).

### Request

{
  "days_before": 7,
  "email_enabled": true,
  "push_enabled": true
}

### Response (updated)

{
  "id": 1,
  "user": 1,
  "days_before": 7,
  "email_enabled": true,
  "push_enabled": true
}

---

## 5.3. PUT/PATCH `/api/notification-settings/{id}/`

Update settings by ID.

---

# 6. Friends System

## FriendRequest Model

{
  "id": 1,
  "from_user": 1,
  "to_user": 2,
  "status": "pending",     // "pending" | "accepted" | "rejected"
  "created_at": "2025-11-20T10:00:00Z"
}

### Rules

* `from_user` is always the authenticated user on creation.
* Unique per pair: a user cannot send two requests to the same person.


## 6.1. GET `/api/friends/`

Return all friend requests involving the authenticated user.

Includes:

* Requests sent **to** user
* Requests sent **by** user

Paginated.

### Example

{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "from_user": 1,
      "to_user": 2,
      "status": "pending",
      "created_at": "2025-11-20T10:00:00Z"
    },
    {
      "id": 2,
      "from_user": 3,
      "to_user": 1,
      "status": "accepted",
      "created_at": "2025-11-19T08:30:00Z"
    }
  ]
}

---

## 6.2. POST `/api/friends/`

Send a new friend request.

### Request

{
  "to_user": 2,
  "status": "pending"
}

Notes:

* `from_user` is ignored.
* `status` defaults to `"pending"`.

---

## 6.3. PATCH `/api/friends/{id}/`

Update friend request status.

### Example

{
  "status": "accepted"
}

---

## 6.4. DELETE `/api/friends/{id}/`

Delete a friend request.

---

# 7. Common Subscriptions

## 7.1. GET `/api/common/`

Return shared active subscriptions with accepted friends, with suggestions.

### Matching Logic

A match occurs if:

* Both subscriptions belong to accepted friends
* Both are active (`is_active = true`)
* Names match case-insensitively:

s1.name.strip().lower() == s2.name.strip().lower()

### Example Response


[
  {
    "friend": "alice",
    "service": "Netflix",
    "you_pay": 12.99,
    "friend_pays": 15.99,
    "suggestion": "Consider using a shared or family plan to reduce costs."
  },
  {
    "friend": "bob",
    "service": "Spotify",
    "you_pay": 4.99,
    "friend_pays": 9.99,
    "suggestion": "Consider using a shared or family plan to reduce costs."
  }
]


---

# 8. Versioning

This file documents **API v1** of Subscription Tracker backend.

Breaking changes MUST be:

* negotiated with frontend, **or**
* introduced as a new API version (v2).

Frontend (web and mobile) should rely on the structure and behavior defined here.


