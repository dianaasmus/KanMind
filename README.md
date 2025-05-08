# KanMind

KanMind is a backend project written in Python with the Django Web Framework and the Django REST Framework (DRF). It provides a structured API for a kanban-inspired task management system.


## 📦 Installation

```bash
git clone https://github.com/dianaasmus/kanmind.git
cd kanmind
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 🚀 Run frontend and backend Server

```bash
task kanmind
```

## ⚙️ Tech Stack

Python 3.11+  
Django 4.x  
Django REST Framework  


## 🎁 Features

🗂 Boards: Organize your tasks into multiple kanban boards  
✅ Tasks: Create, update, and delete tasks with title, description, due date, and more  
📦 Columns/Statuses: Move tasks between status columns (e.g., "Todo", "In Progress", "Done")  
👤 User Accounts (optional): Authentication and user-specific data  
🧩 REST API: Fully built with Django REST Framework — ideal for a decoupled frontend  
🔐 Authentication: Support for TokenAuthentication