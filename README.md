# EventHub - Event Management System

A modern web-based Event Management System developed using Django, PostgreSQL, and Tailwind CSS. The system provides secure authentication, role-based access control, event management, participant registration, attendance management, and user profile management through a responsive and user-friendly interface.

---

# Overview

EventHub is designed to simplify event organization and participation. The system enables administrators and organizers to efficiently manage events while allowing participants to register, manage their profiles, and participate in events securely.

The application follows Django best practices with authentication, authorization, responsive design, and role-based permissions.

---

# Features

## Authentication

- User Registration
- Email Verification
- Login
- Logout
- Forgot Password
- Reset Password
- Change Password
- Password Validation

---

## User Profile

- View Profile
- Edit Profile
- Upload Profile Picture
- Update Phone Number
- Update Address
- Update Bio

---

## Role-Based Access Control

### Administrator

- Dashboard
- Manage Users
- Change User Roles
- Delete Users
- Manage Events
- Manage Categories
- Manage Participants
- Manage Attendance

### Organizer

- Dashboard
- Manage Events
- Manage Categories
- Manage Participants
- Manage Attendance

### Participant

- Dashboard
- Register for Events
- Cancel Event Registration
- View Registered Events
- Manage Personal Profile
- Change Password

---

# Event Management

- Create Events
- Update Events
- Delete Events
- Event Details
- Event Image Upload
- Event Capacity Management
- Automatic Registration Closing
- Full Capacity Detection

---

# Category Management

- Create Categories
- Update Categories
- Delete Categories

---

# Participant Management

- Add Participants
- Update Participants
- Delete Participants
- Upload Participant Profile Image

---

# Attendance Management

- Attendance List
- Mark Attendance
- Export Attendance to PDF
- Export Attendance to Excel

---

# Dashboard

The dashboard provides quick access to important system information, including:

- Total Events
- Total Categories
- Total Participants
- Upcoming Events
- Past Events
- Today's Events

---

# Search and Filtering

- Search Events by Name
- Search by Location
- Filter by Category
- Filter by Date Range
- Pagination

---

# Responsive Design

The application is fully responsive and optimized for:

- Desktop
- Tablet
- Mobile Devices

---

# Technology Stack

## Backend

- Python 3
- Django 6

## Database

- PostgreSQL

## Frontend

- HTML5
- Tailwind CSS
- JavaScript

## Libraries

- Pillow
- ReportLab
- OpenPyXL
- WhiteNoise
- python-dotenv

---

# Installation

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

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file in the project root.

Example:

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

## Run the Development Server

```bash
python manage.py runserver
```

Open the application in your browser:

```
http://127.0.0.1:8000/
```

---

# Project Structure

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

# User Roles and Permissions

| Feature | Admin | Organizer | Participant |
|----------|:-----:|:---------:|:-----------:|
| Dashboard | Yes | Yes | Yes |
| Event Management | Yes | Yes | View/Register |
| Category Management | Yes | Yes | No |
| Participant Management | Yes | Yes | No |
| Attendance Management | Yes | Yes | No |
| User Management | Yes | No | No |
| Change User Role | Yes | No | No |
| Delete User | Yes | No | No |
| Profile Management | No | Yes | Yes |
| Change Password | Yes | Yes | Yes |

---

# Screenshots

Add application screenshots in this section.

```
screenshots/
├── dashboard.png
├── login.png
├── signup.png
├── events.png
├── profile.png
```

---

# Future Improvements

- QR Code Event Check-in
- Email Notifications
- Calendar Integration
- Event Analytics
- REST API
- Mobile Application
- Dark Mode
- Multi-language Support

---

# License

This project was developed for academic and educational purposes.

---

# Author

**Md. Sakibul Hoque**

Department of Computer Science and Engineering

American International University-Bangladesh (AIUB)

GitHub: https://github.com/Sakibul786