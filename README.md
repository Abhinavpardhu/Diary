# 📖 My Diary

A secure and modern diary web application built with **Django**. Users can register, log in, and manage their personal diary entries in a clean and responsive interface.

---

## ✨ Features

* 🔐 User Authentication (Register, Login, Logout)
* 📝 Create diary entries
* ✏️ Edit existing entries
* 🗑️ Delete diary entries
* 📚 View all diary entries
* 👤 User-specific diary (each user sees only their own entries)
* 🎨 Responsive UI using Bootstrap 5
* 🔒 Protected routes using Django Authentication

---

## 🛠️ Tech Stack

* **Backend:** Django
* **Frontend:** HTML, CSS, Bootstrap 5
* **Database:** SQLite3
* **Language:** Python 3

---

## 📂 Project Structure

```
Diary/
│
├── Diary/                 # Django project
│
├── app/                   # Main application
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
│
├── db.sqlite3
├── manage.py
└── README.md
```

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/your-username/Diary.git
```

### Move into the project

```bash
cd Diary
```

### Create a virtual environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Apply migrations

```bash
python manage.py migrate
```

### Run the development server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

## 📷 Screenshots

Add screenshots of:

* Login Page
* Register Page
* Home Page
* Add Diary Entry
* Edit Diary Entry

---

## 🔐 Authentication

The project uses Django's built-in authentication system.

* User Registration
* Login
* Logout
* Password Authentication
* Protected Views (`@login_required`)

---

## 📌 Future Improvements

* Password Reset via Email
* Search Diary Entries
* Categories and Tags
* Rich Text Editor
* Dark Mode
* Calendar View
* Image Uploads
* Export Diary as PDF
* REST API using Django REST Framework

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Abhinav Pardhu**

GitHub: https://github.com/Abhinavpardhu

