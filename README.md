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
├── Admin/
│ ├── ad_approve.php
│ ├── view_ads.php
│ ├── ...
├── User/
│ ├── submit_ad.php
│ ├── view_status.php
│ ├── ...
├── uploads/
│ └── [ad files]
├── css/
│ └── style.css
├── js/
│ └── validation.js
├── includes/
│ └── db.php, functions.php
├── index.php
├── login.php
├── register.php
├── logout.php
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
