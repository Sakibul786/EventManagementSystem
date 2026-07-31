# Event Management System

A web-based Event Management System developed using Django, PostgreSQL, and Tailwind CSS. The system provides role-based access control for administrators, organizers, and participants to efficiently manage events, registrations, and attendance.

---

## Overview

The system allows users to create, manage, and participate in events through a secure and user-friendly interface. It includes authentication, event registration, attendance management, search and filtering, and role-based permissions.

---

## Features

### Authentication

- User Registration
- Login and Logout
- Email Verification
- Password Validation

### Role-Based Access Control

**Administrator**

- Manage Users
- Change User Roles
- Delete Users
- Manage Events
- Manage Categories
- Manage Participants
- Manage Attendance

**Organizer**

- Manage Events
- Manage Categories
- Manage Participants
- View Attendance

**Participant**

- Register for Events
- Cancel Event Registration
- View Registered Events

---

## Event Management

- Create Events
- Update Events
- Delete Events
- Event Details
- Event Image Upload
- Event Capacity Management
- Automatic Registration Closing
- Full Capacity Detection

---

## Category Management

- Create Categories
- Update Categories
- Delete Categories

---

## Participant Management

- Add Participants
- Update Participants
- Delete Participants

---

## Attendance Management

- Attendance List
- Mark Attendance
- Export Attendance to PDF
- Export Attendance to Excel

---

## Dashboard

- Total Events
- Total Categories
- Total Participants
- Upcoming Events
- Past Events
- Today's Events

---

## Search and Filtering

- Search by Event Name
- Search by Location
- Filter by Category
- Filter by Date Range
- Pagination

---

## Technology Stack

- Python 3
- Django 6
- PostgreSQL
- Tailwind CSS
- HTML5
- CSS3
- JavaScript
- Pillow
- ReportLab
- OpenPyXL

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/EventManagementSystem.git

cd EventManagementSystem
```

### Create a Virtual Environment

**Windows**

```bash
python -m venv venv

venv\Scripts\activate
```

**Linux/macOS**

```bash
python3 -m venv venv

source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

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

### Apply Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

### Create a Superuser

```bash
python manage.py createsuperuser
```

### Run the Development Server

```bash
python manage.py runserver
```

Open the application in your browser:

```
http://127.0.0.1:8000/
```

---

## Project Structure

```
EventManagementSystem/
│
├── accounts/
├── config/
├── events/
├── media/
├── static/
├── templates/
├── .env
├── .gitignore
├── manage.py
├── package.json
├── requirements.txt
├── tailwind.config.js
└── README.md
```

---

## User Roles and Permissions

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

---

## Future Improvements

- Email Notifications
- QR Code Event Check-in
- Calendar Integration
- Event Analytics
- REST API
- Mobile Application
- Dark Mode
- Multi-language Support

---

## License

This project was developed for academic and educational purposes.

---

## Author

Md. Sakibul Hoque
American International University Bangladesh (AIUB)
Department of Computer Science and Engineering 

GitHub: https://github.com/Sakibul786