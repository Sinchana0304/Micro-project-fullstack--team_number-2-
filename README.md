# 🌍 Disaster Relief Management System

Disaster Relief Management System is a fullstack Django web application designed to streamline disaster tracking, donation management, and user coordination. Built for quick local setup using SQLite, it supports user authentication, image uploads, and admin oversight. This repository includes the Django project, core app, templates, static assets, and migrations to help you get started.

## 🚀 Features

- Role-based registration for organisers and donors
- Secure login with custom password validation
- Organiser dashboard with sidebar navigation and disaster summaries
- Donor dashboard with donation history and feedback options
- Manual bank transfer donation flow with transaction ID validation
- Messaging system for organiser-donor communication
- Feedback and reporting tools for transparency

## 🛠️ Tech Stack

- **Backend**: Django, SQLite/PostgreSQL
- **Frontend**: HTML, CSS, Bootstrap
- **Authentication**: Django custom user model
- **Payment Flow**: Manual bank transfer with validation
- **Third-party Integration**: Razorpay (optional for future phases)

Core Functionalities
 User Management
- Registration, login, logout
- Profile picture upload
- Role-based access (admin vs regular user)
 Disaster Tracking
- Add disasters with title, description, location, image, and date
- Admin can edit/delete disasters
- Users can view disaster history
 Donation Management
- Users can donate with amount, date, and proof image
- Admin can view and verify donations
- Donation history per user
 Dashboard & Analytics
- Personalized dashboard showing user activity
- Admin dashboard with system-wide stats
- Potential for future visualizations (e.g., donation trends, disaster heatmaps)


## 📦 Installation

```bash
git clone https://github.com/yourusername/disaster-relief.git
cd disaster-relief
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Team Members
Team Number 2

Rachana Gowda Y L  - 4MC23IS084
Reshma S C - 4MC23IS088
Sinchana C S - 4MC23IS105
Thanmayi K Y - 4MC23IS117