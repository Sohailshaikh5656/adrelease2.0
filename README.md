<p align="center">
  <img src="https://static.djangoproject.com/img/logos/django-logo-positive.svg" alt="Django Logo" width="160"/>
</p>

<h1 align="center">📢 AdRelease 2.0</h1>

<p align="center">
  <i>Django-based Newspaper Advertisement Management System</i>
</p>

---

## 📝 Overview

**AdRelease 2.0** is a Django-powered web application for managing newspaper advertisements. It provides a clean user interface for users to submit advertisement requests and an admin panel for managing and approving those ads.

## 🗂️ Folder Structure

adrelease2.0/
├── adrelease2/ # Main project settings
│ ├── init.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── ad/ # App for ad management
│ ├── migrations/
│ ├── templates/
│ ├── static/
│ ├── admin.py
│ ├── models.py
│ ├── views.py
│ └── urls.py
├── media/ # Uploaded ad files
├── static/ # Static files
├── templates/ # Base templates
├── db.sqlite3 # Default database
├── manage.py # Django management script
└── README.md

---


---

## 🚀 How to Run Locally

```bash
# Step 1: Clone the repository
git clone https://github.com/Sohailshaikh5656/adrelease2.0.git
cd adrelease2.0

# Step 2: Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # for Linux/macOS
venv\Scripts\activate      # for Windows

# Step 3: Install dependencies
pip install -r requirements.txt   # (if available)

# Step 4: Run migrations
python manage.py migrate

# Step 5: Start development server
python manage.py runserver

# Step 6: Open in browser
http://127.0.0.1:8000/

👨‍💻 Author
Shaikh Sohel
📘 MCA @ LJ Campus | 💻 Core PHP, Laravel, Node.js

📄 License
This project is open-source and available for learning and academic use.
