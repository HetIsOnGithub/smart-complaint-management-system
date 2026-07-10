# Smart Complaint Management System

A web-based Complaint Management System built using Django that enables users to submit, track, and manage complaints efficiently. The system includes secure authentication, role-based dashboards, image uploads, comments, complaint status tracking, and AI-assisted complaint classification using Google Gemini.

## Features

- User Registration & Login
- Secure Authentication using Django Authentication
- Password Hashing
- User Dashboard
- Admin Dashboard
- Submit Complaint
- AI-generated Complaint Title
- AI-generated Category
- AI-generated Priority
- Complaint Status Tracking
- Upload Complaint Images
- Comment System
- Complaint Details Page
- Admin Complaint Management
- Update Complaint Status
- Delete Complaints
- SQLite Database
- Responsive Bootstrap 5 UI
- CSRF Protection
- Django ORM
- Form Validation

## Tech Stack

### Backend
- Python 3
- Django
- SQLite
- Django ORM

### Frontend
- HTML
- CSS
- Bootstrap 5
- JavaScript

### AI
- Google Gemini API

## Project Structure

```
SmartComplaintManagement/
│
├── SmartComplaintManagement/
├── complaints/
├── templates/
├── static/
├── media/
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/smart-complaint-management-system.git
```

### Move into Project

```bash
cd smart-complaint-management-system
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file and add:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

### Run Migrations

```bash
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Run Server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

## AI Workflow

1. User enters only the complaint description.
2. Google Gemini analyzes the complaint.
3. AI generates:
   - Complaint Title
   - Category
   - Priority
4. Complaint is stored in the database.

If the AI service is temporarily unavailable, the system automatically stores default values to ensure uninterrupted complaint submission.

## Future Improvements

- Email Notifications
- Complaint Search & Filters
- File Attachments
- Complaint Analytics
- Department Allocation
- SMS Notifications
- PostgreSQL Support
- REST API Integration

## License

This project is developed for educational and learning purposes.
