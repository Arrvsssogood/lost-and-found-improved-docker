# 🔍 Finders Keepers — Campus Lost & Found System

A full-stack web application built with Flask, MongoDB, and Docker for managing lost and found items on campus. Users can submit reports, and admins can review, approve, and manage all submissions.

# IMPROVED LOST AND FOUND SYSTEM FROM MY FIRST YEAR DAYS
---

# 🚀 FULL SETUP & RUN GUIDE

## 📦 Requirements

Before running the project, make sure you have:

- Docker
- Docker Compose

Check if they are installed:

docker --version  
docker compose version  

---

# 🏁 HOW TO RUN THE PROJECT (DOCKER)

## 1. Start the application

From the project root folder, run:

docker compose up --build

This will:
- Build the Flask application
- Start the MongoDB container
- Connect both services automatically

---

## 2. Open the application

Once everything is running, open your browser:

http://localhost:5000

---

## 3. Stop the application

To stop all running containers:

docker compose down

To stop and remove all data (including database reset):

docker compose down -v

---

# 👤 DEFAULT ADMIN ACCOUNT

The system automatically creates an admin account on first run:

Username: admin  
Password: admin123  

⚠️ Change this after setup if needed.

---

# 📁 PROJECT STRUCTURE

finders-keepers/  
├── app.py  
├── requirements.txt  
├── Dockerfile  
├── docker-compose.yml  
├── .gitignore  
├── .dockerignore  
└── app/  
  ├── templates/  
  │  ├── base.html  
  │  ├── index.html  
  │  ├── gallery.html  
  │  ├── report.html  
  │  ├── my_items.html  
  │  ├── login.html  
  │  ├── register.html  
  │  ├── admin.html  
  │  ├── admin_edit.html  
  │  ├── admin_create.html  
  │  └── admin_users.html  
  └── static/  
    ├── css/  
    ├── js/  
    └── uploads/  

---

# 🧠 FEATURES

## 👥 User Features
- Register and login system
- Submit lost or found items
- Upload item images
- View and manage personal submissions
- Delete own posts
- Browse and search public gallery

---

## 🛡️ Admin Features
- Admin dashboard access
- View all submitted items
- Approve or reject submissions
- Mark items as claimed or unclaimed
- Edit any item
- Delete any item
- Create items manually
- Manage users

---

## 🔍 Public Gallery
- Search by title, description, or location
- Filter by category
- Filter by item type (lost/found)
- Filter by status (claimed/unclaimed)
- Only approved items are visible publicly

---

# 🗄️ DATABASE (MONGODB)

## Database Name
finders_keepers

---

## USERS COLLECTION

{
  "username": "john",
  "email": "john@school.edu",
  "password": "<hashed_password>",
  "is_admin": false,
  "created_at": "2024-01-01T00:00:00"
}

---

## ITEMS COLLECTION

{
  "title": "Black Wallet",
  "description": "Found near canteen",
  "location": "Main Canteen",
  "category": "Keys/Wallet",
  "item_type": "found",
  "date_found": "2024-01-15",
  "image": "wallet.jpg",
  "status": "pending",
  "claimed": false,
  "submitted_by": "<user_id>",
  "submitted_by_name": "john",
  "created_at": "2024-01-15T12:00:00"
}

---

# ⚙️ RUNNING WITHOUT DOCKER (OPTIONAL DEV MODE)

## 1. Install dependencies

pip install -r requirements.txt

---

## 2. Start MongoDB locally

Make sure MongoDB is running on:

mongodb://mongo:27017/finders_keepers

---

## 3. Run the Flask app

python app.py

Then open:

http://localhost:5000

---

# 🔧 DOCKER COMMANDS SUMMARY

## Build and run
docker compose up --build

## Run in background
docker compose up -d

## Stop containers
docker compose down

## Reset everything (delete database data)
docker compose down -v

---

# 📝 NOTES

- Uploaded images are stored in `app/static/uploads/`
- Admin account is created automatically on first run
- Items start as "pending" until approved by admin
- Only approved items appear in the public gallery
- Rejected items are hidden from users