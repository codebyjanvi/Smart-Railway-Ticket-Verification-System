# Smart Railway Ticket Verification System

## 🚆 Smart Railway Ticket Verification System

A web-based railway ticket booking and verification system developed using **Python Flask, SQLite, HTML, CSS, JavaScript, and QR Code technology**.

The system is designed to make railway ticket verification faster, easier, and more secure by replacing traditional manual ticket checking with **QR-based digital verification**.

---

## 📌 Project Overview

The **Smart Railway Ticket Verification System** provides a complete digital workflow:

**Passenger → Ticket Booking → Passenger Image Capture → Payment Simulation → QR Ticket Generation → TTE QR Scanning → Ticket Verification → Verification Record**

The system supports three main roles:

* 👤 **Passenger**
* 🎫 **TTE (Ticket Examiner)**
* 🛠️ **Admin**

---

## ✨ Features

### 👤 Passenger Module

* Online railway ticket booking
* Passenger details entry
* Passenger image/webcam capture
* Automatic Ticket ID generation
* Automatic PNR generation
* Bogie/coach assignment
* QR-based digital ticket
* PNR status checking
* Ticket cancellation
* Refund amount calculation
* Cancellation receipt
* Refund status display

### 🎫 TTE Module

* Secure TTE login
* QR code scanner
* Instant ticket verification
* Passenger details display
* Passenger image display
* Valid/invalid ticket detection
* Verification history storage

### 🛠️ Admin Module

* Secure admin login
* Dashboard
* Total tickets statistics
* Verified ticket statistics
* Verification history
* System monitoring and reports

---

## 🔐 QR Ticket Verification

Every successful booking generates a unique QR code.

The QR code contains a verification URL associated with the ticket ID.

When the TTE scans the QR code:

1. QR data is decoded.
2. Ticket ID is extracted.
3. Flask searches the SQLite database.
4. Ticket validity is checked.
5. Passenger details are displayed.
6. Passenger image is displayed.
7. Verification is recorded.
8. The TTE receives the verification result.

---

## 💰 Ticket Cancellation & Refund

The system also includes a digital cancellation process.

When a passenger cancels a ticket, the system calculates:

* Original Fare
* Cancellation Charge
* Refund Amount
* Refund Status

Example:

```text
Original Fare       : ₹500
Cancellation Charge : ₹50
Refund Amount       : ₹450
Refund Status       : Processing
```

The cancellation page displays a digital cancellation receipt after successful cancellation.

---

## 🏗️ System Architecture

```text
                 ┌─────────────────────┐
                 │      Passenger      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Flask Web App     │
                 └──────────┬──────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
       ┌───────────┐  ┌───────────┐  ┌────────────┐
       │  Booking  │  │ QR System │  │ Cancellation│
       └─────┬─────┘  └─────┬─────┘  └──────┬─────┘
             │              │               │
             └──────────────┼───────────────┘
                            ▼
                   ┌─────────────────┐
                   │  SQLite Database│
                   └────────┬────────┘
                            │
                    ┌───────┴────────┐
                    ▼                ▼
              ┌──────────┐     ┌──────────┐
              │    TTE   │     │  Admin   │
              │  Scanner │     │Dashboard │
              └──────────┘     └──────────┘
```

---

## 🛠️ Technology Stack

| Technology   | Purpose                         |
| ------------ | ------------------------------- |
| Python       | Backend programming             |
| Flask        | Web application framework       |
| SQLite       | Database                        |
| HTML5        | Web page structure              |
| CSS3         | UI design                       |
| JavaScript   | Dynamic functionality           |
| Bootstrap    | Responsive interface            |
| QR Code      | Digital ticket verification     |
| OpenCV       | Image processing/camera support |
| html5-qrcode | Browser QR scanning             |

---

## 📂 Project Structure

```text
Smart-Railway-Ticket-Verification-System/
│
├── app.py
├── requirements.txt
├── README.md
│
├── railway.db
│
├── static/
│   ├── css/
│   ├── js/
│   ├── faces/
│   └── qr/
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── booking.html
│   ├── ticket.html
│   ├── scan.html
│   ├── verify.html
│   ├── cancel_ticket.html
│   ├── pnr_status.html
│   ├── tte_dashboard.html
│   └── admin_dashboard.html
│
└── README.md
```

---

## 🗄️ Database

The project uses SQLite.

### Main Tables

### `tickets`

Stores passenger and ticket information.

```text
ticket_id
name
phone
source
destination
date
seat
bogie
pnr
is_used
is_fraud
face_image
```

### `users`

Stores system users.

```text
id
username
password
role
```

### `verified_tickets`

Stores ticket verification history.

```text
id
ticket_id
name
phone
source
destination
date
seat
bogie
pnr
face_image
verified_time
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Smart-Railway-Ticket-Verification-System.git
```

### 2. Open the project

```bash
cd Smart-Railway-Ticket-Verification-System
```

### 3. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

### 6. Open in browser

```text
http://127.0.0.1:5000
```

---

## 📦 Requirements

Example `requirements.txt`:

```text
Flask
qrcode
Pillow
opencv-python
```

Install using:

```bash
pip install -r requirements.txt
```

---

## 🔄 Main System Workflow

### Ticket Booking

```text
Enter Passenger Details
        ↓
Capture Passenger Image
        ↓
Generate Ticket ID
        ↓
Generate PNR
        ↓
Assign Seat/Bogie
        ↓
Payment Simulation
        ↓
Generate QR Code
        ↓
Display Digital Ticket
```

### Ticket Verification

```text
TTE Login
    ↓
Open QR Scanner
    ↓
Scan Passenger QR
    ↓
Find Ticket in Database
    ↓
Check Ticket Validity
    ↓
Display Passenger Details
    ↓
Display Passenger Image
    ↓
Store Verification Record
```

### Ticket Cancellation

```text
Enter Ticket ID
       ↓
Find Ticket
       ↓
Calculate Cancellation Charge
       ↓
Calculate Refund
       ↓
Cancel Ticket
       ↓
Display Cancellation Receipt
       ↓
Show Refund Status
```

---

## 🔒 Security Considerations

The current project is an academic prototype. For production deployment, the following should be added:

* Password hashing using bcrypt
* HTTPS
* CSRF protection
* Secure session management
* OTP-based authentication
* Input validation
* Rate limiting
* Database backups
* Production-grade database such as PostgreSQL/MySQL

---

## ⚠️ Current Limitations

* No live Indian Railways/IRCTC API integration
* Payment is simulated
* SQLite is intended for prototype/small-scale use
* Face recognition is not required for the final QR verification workflow
* No official railway reservation integration
* Refund processing is simulated and does not perform a real bank/UPI transaction
* Production deployment requires additional security measures

---

## 🔮 Future Enhancements

* Indian Railways/IRCTC API integration
* Real-time train availability
* Real PNR status
* Real UPI/payment gateway integration
* PostgreSQL/MySQL migration
* Cloud deployment
* Android/iOS application
* Offline TTE verification
* Advanced fraud detection
* AI-based passenger verification
* SMS/email notifications
* Multi-language support
* Advanced analytics
* Real refund/payment integration

---

## 🎓 Academic Project

**Project:** Smart Railway Ticket Verification System

**Course:** Bachelor of Computer Applications (BCA)

**College:** A.G.M BBA & BCA College, Varur

**Academic Year:** 2025–2026

---

## 👩‍💻 Project Status

**Status:** Completed Academic Prototype

The project demonstrates the practical implementation of:

* Web application development
* Flask backend development
* SQLite database management
* QR code generation
* QR-based ticket verification
* Passenger image capture
* Ticket cancellation
* Refund calculation
* Role-based dashboards
* Digital record management

---

## 📄 License

This project is developed for **academic and educational purposes**.
