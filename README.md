# 🛡️ TwinGuard
### AI-Powered Evil Twin Wi-Fi Detection & Secure Connection System

> Detect. Analyze. Protect.

TwinGuard is a Windows-based cybersecurity application that helps users identify **Fake Wi-Fi (Evil Twin) Access Points** before connecting. It scans nearby wireless networks, analyzes suspicious characteristics such as duplicate SSIDs, MAC address mismatches, security inconsistencies, and signal anomalies, then alerts users in real time to reduce the risk of Man-in-the-Middle (MITM) attacks.

---

# 🚀 Features

### 📡 Real-Time Wi-Fi Scanning
- Scan nearby Wi-Fi networks
- View SSID, BSSID (MAC), Signal Strength, Channel, and Security
- Detect currently connected network

### 🛡️ Evil Twin Detection
TwinGuard identifies suspicious networks using multiple heuristics:

- Duplicate SSIDs
- Different MAC addresses
- Security mismatches
- Signal strength anomalies
- Vendor inconsistencies

### 🔒 Secure Connection Management
- Connect to secured Wi-Fi
- Connect to open Wi-Fi
- Disconnect from current Wi-Fi
- Password popup before connecting

### 📊 Live Dashboard
- Connected Network Status
- Number of Networks Found
- Safe Networks
- Suspicious Networks
- Scan Timestamp

### 📜 Scan History
- Session-based scan history
- Threat log
- Export scan results to CSV

### ⚠️ Threat Analysis
Each suspicious network includes:
- Threat Level
- Detection Reason
- Safety Recommendation

### 🎨 Modern User Interface
- Clean responsive design
- Interactive status cards
- Animated notifications
- Threat drawer
- Password modal
- Auto scan


---

# 🏗️ Project Architecture

```
TwinGuard
│
├── app.py
│
├── scanner.py
│
├── detector.py
│
├── templates/
│      landing.html
│      index.html
│
└── README.md
```

---

# ⚙️ Technology Stack

## Frontend
- HTML5
- CSS3
- JavaScript
- Font Awesome

## Backend
- Python
- Flask

## Networking
- Windows netsh Commands

## Detection
- Custom Rule-Based Detection Engine

---

# 🔍 Detection Strategy

TwinGuard identifies suspicious Wi-Fi networks using:

- Duplicate SSID Detection
- MAC Address Comparison
- Vendor Identification
- Security Authentication Comparison
- Channel Analysis
- Signal Strength Evaluation

The application classifies networks as:

- ✅ Safe
- ⚠️ Security Mismatch
- 🚨 Possible Evil Twin

---

# 📂 How It Works

```
User

↓

Scan Networks

↓

Windows netsh

↓

Network Information

↓

TwinGuard Detection Engine

↓

Threat Analysis

↓

Dashboard

↓

Connect / Disconnect
```

---

# 💻 Installation

Clone the repository

```bash
git clone https://github.com/priyapulakhandam/TwinGuard.git
```

Move into the project

```bash
cd TwinGuard
```

Install dependencies

```bash
pip install flask
```

Run the application

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

# 📌 Requirements

- Windows 10 / Windows 11
- Python 3.10+
- Flask
- Wireless Adapter
- Administrator Privileges (Recommended)

---

# 📊 Current Functionalities

- Scan Wi-Fi Networks
- Detect Fake Access Points
- Connect to Networks
- Disconnect Networks
- Export CSV Reports
- Session Scan History
- Connected Network Detection
- Real-Time Dashboard
- Safety Guidelines
- Threat Explanation

---

# 🔐 Security Note

TwinGuard does **not** collect passwords or upload Wi-Fi information to external servers.

All detection is performed **locally** on the user's machine.

---

# 🚀 Future Enhancements

## Mobile Version
- React Native
- Android Support

## Backend Upgrade
- Django REST Framework
- PostgreSQL

## AI Features
- Machine Learning Threat Detection
- Risk Prediction
- Behavioral Analysis

## Cloud Features
- User Accounts
- Scan Synchronization
- Threat Intelligence Database

## Additional Features
- PDF Reports
- Email Alerts
- Real-Time Notifications
- Auto Block Suspicious Networks
- WPA3 Detection
- Vendor Database
- Offline SQLite Storage

---

# ⭐ Support

If you found this project useful,

⭐ Star this repository

🍴 Fork it

📢 Share it with others

---

# 📜 License

This project is licensed under the MIT License.

---

## 🌟 TwinGuard

**Protecting users from Fake Wi-Fi threats - one network at a time.**
