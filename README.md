# 📚 Book Review Management System

A Flask-based web application for managing book reviews. Includes user authentication, CRUD operations, custom error handling, and is Docker-ready for easy deployment.

---

## 🚀 Features

- ✅ User login with session management (cookie-based)
- ✅ Create, read, update, and delete (CRUD) book reviews
- ✅ Secure sessions with configurable `secret_key`
- ✅ Client-side and server-side input validation
- ✅ Custom 404 and error pages
- ✅ Dockerized for deployment ease

---

## 🛠️ Tech Stack

- **Backend**: Python 3.9+, Flask
- **Frontend**: Jinja2 Templates, HTML/CSS (Bootstrap optional)
- **Database**: SQLite
- **Containerization**: Docker

---

## ⚙️ Setup & Running

### 📦 Prerequisites

- [Docker](https://www.docker.com/) (for containerized setup)
- Or, Python 3.9+ & pip (for local setup)

---

### 🔧 Installation

#### 🔹 Clone the repository

```
git clone <repository-url>
cd book-review-system
````

---

### 🐳 Run with Docker

```
docker build -t book-review-system .
docker run -p 5000:5000 book-review-system
```

Open your browser: [http://localhost:5000](http://localhost:5000)
Default login credentials:

* **Username**: `admin`
* **Password**: `password`

---

### 🖥️ Run Locally

```
pip install -r requirements.txt
python app.py
```

Ensure `app.secret_key` is securely set inside `app.py` or via environment variable `FLASK_SECRET_KEY`.

---

## 🧪 Testing (Manual)

1. Log in using the default credentials.
2. Add a new book review.
3. Edit or delete the review.
4. Test invalid inputs for form validation.
5. Try accessing routes like `/add` without logging in to test session protection.
6. Visit a non-existent URL to see the custom error page.

---

## 📊 UML Diagrams

Diagrams illustrating system design are available in the `diagrams/` folder:

* **Use Case Diagram**: User login, add/edit/delete review.
* **Class Diagram**: Classes like `User`, `Review`, `Session`.
* **Sequence Diagram**: Flow of adding a new review.

These are written in [PlantUML](https://plantuml.com/) format.

---

## 🛡️ Security Notes

* Sessions are stored in cookies and signed using `Flask.secret_key`
* Use `SESSION_COOKIE_SECURE=True` in production
* Update `secret_key` before deploying to prevent session hijacking

---

## 📁 Project Structure

```
book-review-system/
├── app.py                # Main Flask app
├── requirements.txt      # Dependencies
├── templates/            # HTML templates
├── static/               # CSS, JS (if needed)
├── diagrams/             # UML diagrams (PlantUML format)
└── Dockerfile            # Docker configuration
```

---


## 🙌 Credits

Developed by Failures.
Feel free to contribute or raise issues to improve the project!

```


