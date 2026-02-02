# SIFESS - Anonymous Confessions

SIFESS is a playful, secure, anonymous confession web app built with Django.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- SQLite (Default) or PostgreSQL (configured in .env)

### Installation

1. **Clone & Setup:**
   ```bash
   git clone <repo>
   cd sifess
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
   *(Note: A `requirements.txt` should be generated with `pip freeze > requirements.txt`)*

2. **Environment Variables:**
   Check `.env` file. Simplest setup:
   ```env
   DEBUG=True
   SECRET_KEY=dev-secret
   DATABASE_URL=sqlite:///db.sqlite3
   ```

3. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Start Server:**
   ```bash
   python manage.py runserver
   ```

5. **Visit:** `http://localhost:8000`

## 🧠 Tech Stack
- **Backend:** Django 4.2
- **Frontend:** Django Templates + Tailwind CSS (via CDN) + Alpine.js + HTMX
- **Database:** SQLite (Dev) / PostgreSQL (Prod)
- **Security:** Fernet symmetric encryption for messages.

## ✨ Features
- **Anonymous Messaging**: Send messages to any user via `sifess.app/u/<slug>`.
- **Encryption**: Messages are encrypted at rest.
- **Cartoon UI**: Playful design with animations.

## 🛡️ License
MIT
