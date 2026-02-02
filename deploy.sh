#!/bin/bash

# ==========================================
# SIFESS DEPLOYMENT SCRIPT
# ==========================================

# ⚠️  CONFIGURATION (Please Edit)
PROJECT_DIR=$(pwd)
VENV_ACTIVATE="$PROJECT_DIR/venv/bin/activate"
SERVICE_NAME="sifess"  # Systemd service name (e.g., gunicorn or sifess)

echo "🚀 Starting Deployment for SIFESS..."

# 1. Pull latest code
echo "📦 Pulling latest code..."
git pull origin main

# 2. Activate Virtual Env
if [ -f "$VENV_ACTIVATE" ]; then
    echo "🐍 Activating virtual environment..."
    source "$VENV_ACTIVATE"
else
    echo "❌ Virtual environment not found at $VENV_ACTIVATE"
    exit 1
fi

# 3. Install Dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# 4. Migrate Database
echo "🗄️ Applying migrations..."
python manage.py migrate

# 5. Collect Static Files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# 6. Restart Service (Needs Sudo)
echo "🔄 Restarting application service ($SERVICE_NAME)..."
if systemctl list-units --full -all | grep -Fq "$SERVICE_NAME.service"; then
    sudo systemctl restart $SERVICE_NAME
    echo "✅ Service restarted."
else
    echo "⚠️  Service '$SERVICE_NAME' not found. Please restart manually if needed."
    echo "   (Example: sudo systemctl restart gunicorn)"
fi

echo "✅ Deployment Complete!"
