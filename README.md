# ⚡ Smart AI-Based Ration Billing System
### Face Recognition & QR Code | Tamil Nadu PDS Portal Style

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)

---

## 📌 Project Overview

A fully functional **AI-powered Smart Ration Shop System** that replaces traditional manual verification methods in India's Public Distribution System (PDS). The system uses **face recognition**, **QR code scanning**, and **automated billing** to authenticate beneficiaries and manage monthly ration quotas .

Designed with a **Tamil Nadu Government Portal** aesthetic and integrated with **Thirukkural** quotes throughout the interface.

---

## 🎯 Objectives
-Replace traditional biometric systems with AI-based face recognition integrated with QR authentication
- Automate quota tracking and billing
- Send instant email notifications after every transaction
- Provide a secure, user-friendly shopkeeper interface

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔐 Shop Login | Secure shopkeeper authentication with captcha |
| 📱 QR Code Scanner | Webcam-based ration card scanning |
| 👤 Face Recognition | Live face verification using OpenCV LBPH |
| 👨‍👩‍👧 Family Management | Family-wise member selection and verification |
| 🌾 Smart Billing | Quota check, deduction and bill generation |
| 📊 Family Quota | Shared monthly quota per ration card |
| 📧 Email Notification | Automatic bill notification via Gmail SMTP |
| 🧾 Print Receipt | Printable bill receipt after every transaction |
| 🇮🇳 TN Portal UI | Tamil Nadu government portal style interface |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| Database | MySQL |
| Face Recognition | OpenCV (LBPH Algorithm) |
| QR Code | qrcode (generation), OpenCV QRCodeDetector (scanning) |
| Email | Python smtplib (Gmail SMTP) |
| Environment | python-dotenv |

---

## 📁 Project Structure

```
ration_system/
│
├── app.py                  # Main Flask application
├── config.py               # Configuration loader
├── .env                    # Environment variables (not pushed)
├── .env.example            # Environment template
├── .gitignore
│
├── routes/
│   ├── __init__.py
│   ├── auth.py             # Shop login/logout
│   ├── members.py          # Fetch family members
│   ├── face.py             # Face verification
│   ├── billing.py          # Quota + bill generation
│   └── qr.py              # QR code scanning
│
├── utils/
│   ├── __init__.py
│   ├── db.py               # MySQL connection helper
│   ├── face_utils.py       # OpenCV face logic
│   ├── face_register.py    # Face registration script
│   ├── qr_generator.py     # QR code generator
│   ├── qr_scanner.py       # Webcam QR scanner
│   └── notify.py           # Email notification
│
├── static/
│   ├── faces/              # Registered face images (gitignored)
│   └── qrcodes/            # Generated QR codes (gitignored)
│
└── templates/
    ├── login.html          # Shop login page
    ├── scan.html           # QR scanner page
    ├── members.html        # Family member selection
    ├── verify.html         # Face verification
    └── billing.html        # Billing + receipt
```

---
## 📸 Screenshots

| Login | QR Scan | Face Verification | Billing |
|------|--------|------------------|--------|
| <img src="https://github.com/user-attachments/assets/6af2879a-87b2-4a31-877f-67ca0e8ec4fa" width="300"/> | <img src="https://github.com/user-attachments/assets/8a46f97f-607e-440c-96d4-c49c3ab4eab1" width="300"/> | <img src="https://github.com/user-attachments/assets/bea22c23-d55f-4ddf-a52e-a2d7d1ad35a3" width="300"/> | <img src="https://github.com/user-attachments/assets/3228e7f4-7175-4d7a-8609-dde4dc066e56" width="300"/> |
## ⚙️ Installation & Setup

### Prerequisites
- Python 3.12+
- MySQL 8.0+
- Webcam

### Step 1 — Clone the Repository
```bash
git clone https://github.com/Naresh-Y4/smartpds.git
cd ration-system
```

### Step 2 — Install Dependencies
```bash
pip install flask mysql-connector-python opencv-python opencv-contrib-python qrcode python-dotenv
```

### Step 3 — Configure Environment
Copy `.env.example` to `.env` and fill in your details:
```bash
cp .env.example .env
```

Edit `.env`:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=ration_system
SECRET_KEY=your_secret_key
EMAIL_SENDER=your_gmail@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
```

### Step 4 — Setup Database
Open MySQL Workbench and run `database.sql` to create all tables and sample data.

### Step 5 — Generate QR Codes
```bash
python utils/qr_generator.py
```

### Step 6 — Register Faces
```bash
python -m utils.face_register
```
Enter member ID when prompted. Press **SPACE** to capture face.

### Step 7 — Run the Application
```bash
python app.py
```

Visit: `http://127.0.0.1:5000`

---

## 🗄️ Database Schema

```
shops           → Shop authentication
ration_cards    → QR-linked ration cards
family_members  → Individual member details + face image path
family_quota    → Shared monthly quota per ration card
transactions    → All billing records
```

---

## 🔄 System Workflow

```
Shop Login
    ↓
QR Code Scan (Webcam)
    ↓
Family Member Selection
    ↓
Face Verification (OpenCV LBPH)
    ↓
Item Selection + Quota Check
    ↓
Bill Generation + DB Update
    ↓
Email Notification (Gmail SMTP)
    ↓
Print Receipt
```

---

## 📸 Face Recognition

The system uses **OpenCV's LBPH (Local Binary Pattern Histogram)** algorithm:
- No external hardware required
- Works with standard laptop webcam
- Stores one reference image per member
- Confidence threshold: configurable (default < 80 indicates a valid match)

---

## 📧 Email Notification

After every successful transaction:
- System checks if member has email in database
- If yes → sends HTML bill via Gmail SMTP
- Email includes Bill ID, items purchased, Thirukkural quote
- Notification status saved in transactions table

---

## 🔒 Security

- Shop login with captcha verification
- Face verification before every transaction
- Passwords stored in `.env` (never committed to Git)
- Face images excluded from version control
- Session-based shopkeeper authentication

---

## 🚀 Future Enhancements
- [ ] Deploy in hardware 
- [ ] PDF bill generation
- [ ] Admin dashboard with analytics
- [ ] Monthly quota auto-reset
- [ ] Aadhaar integration
- [ ] SMS notification via Twilio

---

## 👨‍💻 Developer

**Naresh Y**
- 📧 mr.nareshy006@gmail.com
- 📱 8807496177
- 🏫 Skill development project

---

## 📜 Thirukkural

> *உதவி வரைத்தன்று உதவி உதவி செயப்பட்டார் சால்பின் வரைத்து*
>
> *"The worth of help is not measured by its size, but by the greatness of those who receive it."*
> — Thirukkural 101

---
## 📄 License
This project is for educational purposes only.

*© 2026 Smart PDS System — Government of Tamil Nadu Style Interface*
