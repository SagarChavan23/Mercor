# 🕒 Mercor Time Tracker

A full-stack time tracking and productivity management application built using the **T3 Stack** (Next.js, Tailwind CSS, TypeScript, tRPC, Prisma) for the frontend and **Django REST Framework** for the backend.

---

## 🚀 Features

- 👥 Employee management (invite, list, deactivate)
- 📂 Project and task management
- ⏱️ Time tracking with window-level tracking
- 🔐 JWT-based secure authentication
- 🌐 REST API powered by Django and DRF

---

## 🧰 Tech Stack

### Frontend
- [Next.js](https://nextjs.org/)
- [TypeScript](https://www.typescriptlang.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [tRPC](https://trpc.io/)
- [Prisma](https://www.prisma.io/)

### Backend
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)

### Database
- PostgreSQL

---

## 🛠️ Getting Started

### Backend (Django)

```bash
# Navigate to the backend folder
cd backend

# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser

# Run the server
python manage.py runserver


# Navigate to frontend folder
cd t3-app


# Install dependencies
npm install

# Run development server
npm run dev


## API Overview

/api/employees/
/api/projects/
/api/tasks/
/api/time-entries/
All secured endpoints require a JWT token.