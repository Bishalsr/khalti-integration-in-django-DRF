# 💳 Khalti Payment Integration with Django REST Framework (DRF)

A complete backend integration of **Khalti ePayment (Sandbox)** using **Django REST Framework**.

-https://docs.khalti.com/khalti-epayment/

This project demonstrates how to:

- ✅ Initiate Khalti payment from backend
- ✅ Verify payment using `pidx`
- ✅ Store transaction details in database
- ✅ Securely manage secret keys using `.env`
- ✅ Test everything using Postman (No frontend required)

---

## 🚀 Features

- Khalti Sandbox Integration
- Payment Initiation API
- Payment Verification (Lookup) API
- Database Storage for Transactions
- Environment Variable Support
- Clean DRF Architecture

---

## 🛠 Tech Stack

- Python 3.11+
- Django
- Django REST Framework
- Requests Library
- SQLite (Default DB)
- Khalti Sandbox API

---

# 📂 Project Structure

```
khalti-integration-in-django-DRF/
│
├── khalti_core/              # Main Django Project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── payments/                 # Payment App
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
│
├── .env                      # Environment Variables (Not pushed)
├── .gitignore
├── db.sqlite3
├── manage.py
└── README.md
```

---

# ⚙️ Installation Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Bishalsr/khalti-integration-in-django-DRF.git
cd khalti-integration-in-django-DRF
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install django djangorestframework requests python-dotenv
```

Or if `requirements.txt` exists:

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Setup Environment Variables

Create a file named `.env` in your root directory:

```
KHALTI_SECRET_KEY=your_sandbox_secret_key_here
KHALTI_BASE_URL=https://dev.khalti.com/api/v2/epayment/
```

---

## 5️⃣ Update `settings.py`

Add this inside your `settings.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

KHALTI_SECRET_KEY = os.getenv("KHALTI_SECRET_KEY")
KHALTI_BASE_URL = os.getenv("KHALTI_BASE_URL")
```

⚠️ Important: Never push `.env` to GitHub.

---

## 6️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 7️⃣ Run Development Server

```bash
python manage.py runserver
```

Server will start at:

```
http://127.0.0.1:8000/
```

---

# 💰 API Endpoints

Base URL:

```
http://127.0.0.1:8000/api/
```

---

## 1️⃣ Initiate Payment

**POST**
```
/api/khalti/initiate/
```

### Request Body (JSON)

```json
{
  "amount": 1000,
  "purchase_order_name": "Test Product"
}
```

### Successful Response

```json
{
  "pidx": "PnuBtJkEgGwSR",
  "payment_url": "https://test-pay.khalti.com/?pidx=PnuBtJ223322kEgGwSR",
  "expires_at": "2026-02-11T11:47:26.462433+05:45",
  "expires_in": 1800
}
```

👉 Open `payment_url` in browser to complete payment.

---

## 2️⃣ Verify / Lookup Payment

After payment is completed:

**POST**
```
/api/khalti/lookup/
```

### Request Body

```json
{
  "pidx": "PnuBtJkEgG2pwSR"
}
```

This verifies payment with Khalti and updates database status.

---

# 🔐 Authentication

Currently using:

```
permission_classes = [AllowAny]
```

So you can test using Postman without authentication.

For production:
- Add JWT Authentication
- Protect endpoints
- Add Webhook verification

---

# 🧪 Testing with Postman

1. Start Django server
2. Send POST request to `/api/khalti/initiate/`
3. Copy `payment_url`
4. Complete sandbox payment
5. Send POST to `/api/khalti/lookup/` with `pidx`
6. Payment status will update

---

# 🧾 Payment Model Example

```python
class Payment(models.Model):
    purchase_order_id = models.CharField(max_length=255)
    pidx = models.CharField(max_length=255)
    amount = models.IntegerField()
    status = models.CharField(max_length=50, default="Initiated")
    transaction_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.purchase_order_id
```

---

# 🛡 .gitignore Example

```
venv/
__pycache__/
db.sqlite3
.env
*.pyc
```

---

# 🌍 Khalti Sandbox Details

Base URL:

```
https://dev.khalti.com/api/v2/epayment/
```

Sandbox Payment Page:

```
https://test-pay.khalti.com/
```

---

# 🔮 Future Improvements

- JWT Authentication
- Webhook Integration
- Production Deployment
- Subscription Payment
- Dockerization
- Logging & Error Handling



⭐ If this project helped you, please give it a star!
