# 🎉 EventHub - Event Management System

A modern, full-featured **Event Management System** built with **Django**, **PostgreSQL**, and **Tailwind CSS**. EventHub provides a secure, role-based platform for administrators, organizers, and participants to manage events, registrations, attendance, and user profiles.

---

## 📌 Overview

EventHub streamlines the event management process by allowing administrators and organizers to create and manage events while participants can register, manage their profiles, and track their event participation.

The project follows Django best practices with authentication, authorization, responsive UI, and role-based access control.

---

# ✨ Features

## 🔐 Authentication & User Management

- User Registration
- Email Verification
- Login & Logout
- Change Password
- Forgot Password
- Reset Password via Email
- Password Validation
- User Profile Management
- Profile Picture Upload
- Edit Profile Information

---

## 👥 Role-Based Access Control

### 👑 Administrator

- Dashboard
- Manage Users
- Change User Roles
- Delete Users
- Manage Events
- Manage Categories
- Manage Participants
- Manage Attendance

### 🎯 Organizer

- Dashboard
- Manage Events
- Manage Categories
- Manage Participants
- View & Manage Attendance

### 🙋 Participant

- Dashboard
- Register for Events
- Cancel Event Registration
- View Registered Events
- Manage Personal Profile
- Update Profile Picture
- Change Password

---

# 📅 Event Management

- Create Events
- Edit Events
- Delete Events
- Event Image Upload
- Event Capacity Management
- Automatic Registration Closing
- Registration Status
- Full Capacity Detection
- Event Details

---

# 🏷️ Category Management

- Create Categories
- Edit Categories
- Delete Categories

---

# 👤 Participant Management

- Add Participants
- Edit Participants
- Delete Participants
- Upload Profile Picture
- Manage Contact Information

---

# ✅ Attendance Management

- Attendance List
- Mark Attendance
- Update Attendance
- Export Attendance to PDF
- Export Attendance to Excel

---

# 📊 Dashboard

Dashboard includes:

- Total Events
- Total Categories
- Total Participants
- Upcoming Events
- Past Events
- Today's Events

---

# 🔍 Search & Filtering

- Search Events
- Search by Location
- Filter by Category
- Filter by Date Range
- Pagination

---

# 📱 Responsive Design

- Desktop Friendly
- Tablet Friendly
- Mobile Responsive
- Modern UI using Tailwind CSS

---

# 🛠 Technology Stack

### Backend

- Python 3
- Django 6

### Database

- PostgreSQL

### Frontend

- HTML5
- Tailwind CSS
- JavaScript

### Libraries

- Pillow
- ReportLab
- OpenPyXL
- WhiteNoise
- python-dotenv

---

# 📂 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/EventManagementSystem.git

cd EventManagementSystem
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Requirements

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file in the project root.

```env
SECRET_KEY=your-secret-key

DEBUG=True

ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=event_management_db
DB_USER=postgres
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5433

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
```

---

## Apply Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

---

## Create Superuser

```bash
python manage.py createsuperuser
```

---

## Run Development Server

```bash
python manage.py runserver
```

Open your browser:

```
http://127.0.0.1:8000/
```

---

# 📁 Project Structure

```
EventManagementSystem/
│
├── accounts/
├── config/
├── dashboard/
├── events/
├── media/
├── static/
├── templates/
│
├── .env
├── .gitignore
├── manage.py
├── package.json
├── requirements.txt
├── tailwind.config.js
└── README.md
```

---

# 🔑 User Permissions

| Feature | Admin | Organizer | Participant |
|----------|:-----:|:---------:|:-----------:|
| Dashboard | ✅ | ✅ | ✅ |
| Event Management | ✅ | ✅ | View/Register |
| Category Management | ✅ | ✅ | ❌ |
| Participant Management | ✅ | ✅ | ❌ |
| Attendance Management | ✅ | ✅ | ❌ |
| User Management | ✅ | ❌ | ❌ |
| Change User Role | ✅ | ❌ | ❌ |
| Delete User | ✅ | ❌ | ❌ |
| Profile Management | ❌ | ✅ | ✅ |
| Change Password | ✅ | ✅ | ✅ |

---

# 📸 Screenshots

You can add screenshots here.

```
screenshots/
├── dashboard.png
├── login.png
├── signup.png
├── events.png
├── profile.png
```

---

# 🚀 Future Improvements

- QR Code Event Check-in
- Email Notifications
- Calendar Integration
- Event Analytics
- REST API
- Mobile Application
- Dark Mode
- Multi-language Support

---

# 📄 License

This project was developed for academic and educational purposes.

---

# 👨‍💻 Author

**Md. Sakibul Hoque**

Department of Computer Science and Engineering

American International University-Bangladesh (AIUB)

GitHub: https://github.com/Sakibul786