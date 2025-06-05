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

## 🧑‍💻 How to Run Locally

```bash
# Step 1: Clone the repository
git clone https://github.com/Sohailshaikh5656/adrelease2.0.git

# Step 2: Move to XAMPP's htdocs folder
mv adrelease2.0/ /xampp/htdocs/

# Step 3: Start Apache and MySQL via XAMPP

# Step 4: Create a database in phpMyAdmin (e.g., adrelease)
#         Import database.sql (if available)

# Step 5: Update DB credentials in includes/db.php

# Step 6: Run in browser:
http://localhost/adrelease2.0/

👨‍💻 Author
Shaikh Sohel
📘 MCA @ LJ Campus | 💻 Core PHP, Laravel, Node.js

📄 License
This project is open-source and available for learning and academic use.
