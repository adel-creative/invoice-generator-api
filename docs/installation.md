# 💿 Installation Guide

Complete installation instructions for all platforms.

---

## 📋 System Requirements

### Minimum Requirements
- **Python:** 3.11 or higher
- **RAM:** 512 MB
- **Disk Space:** 500 MB
- **OS:** Windows 10+, macOS 10.15+, Ubuntu 20.04+

### Recommended
- **Python:** 3.12
- **RAM:** 2 GB
- **Disk Space:** 2 GB
- **OS:** Latest stable version

---

## 🐧 Linux (Ubuntu/Debian)

### 1. Update System
```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Install Python 3.11+
```bash
sudo apt install python3.11 python3.11-venv python3-pip -y
```

### 3. Install System Dependencies (for WeasyPrint)
```bash
sudo apt install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libfribidi0 \
    libgdk-pixbuf2.0-0 \
    libcairo2 \
    shared-mime-info
```

### 4. Clone Repository
```bash
git clone https://github.com/yourusername/invoice-api.git
cd invoice-api
```

### 5. Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

### 6. Configure Environment
```bash
nano .env
# Edit with your settings
```

### 7. Run Application
```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

---

## 🍎 macOS

### 1. Install Homebrew (if not installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Python 3.11+
```bash
brew install python@3.11
```

### 3. Install System Dependencies
```bash
brew install cairo pango gdk-pixbuf libffi
```

### 4. Clone Repository
```bash
git clone https://github.com/yourusername/invoice-api.git
cd invoice-api
```

### 5. Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

### 6. Configure Environment
```bash
nano .env
# or use any text editor
code .env  # if using VS Code
```

### 7. Run Application
```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

---

## 🪟 Windows

### 1. Install Python 3.11+
- Download from https://www.python.org/downloads/
- **Important:** Check "Add Python to PATH" during installation

### 2. Install Git (optional)
- Download from https://git-scm.com/download/win

### 3. Clone Repository
```powershell
# Using Git
git clone https://github.com/yourusername/invoice-api.git
cd invoice-api

# Or download ZIP and extract
```

### 4. Create Virtual Environment
```powershell
python -m venv venv
```

### 5. Activate Virtual Environment
```powershell
venv\Scripts\activate
```

### 6. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 7. Configure Environment
```powershell
copy .env.example .env
notepad .env
# Edit with your settings
```

### 8. Initialize Database
```powershell
python -c "from app.database import init_db; init_db()"
```

### 9. Run Application
```powershell
uvicorn app.main:app --reload
```

---

## 🐳 Docker Installation

### Prerequisites
- Docker installed
- Docker Compose installed

### Quick Start
```bash
# Clone repository
git clone https://github.com/yourusername/invoice-api.git
cd invoice-api

# Copy environment file
cp .env.example .env
# Edit .env with your settings

# Start with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Manual Docker Build
```bash
# Build image
docker build -t invoice-api:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name invoice-api \
  invoice-api:latest

# View logs
docker logs -f invoice-api

# Stop container
docker stop invoice-api
```

---

## ☁️ Cloud Platforms

### Railway.app
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

### Render.com
1. Connect GitHub repository
2. Select "Web Service"
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables
5. Deploy

### Heroku
```bash
# Install Heroku CLI
# Download from https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Deploy
git push heroku main
```

---

## 🔧 Post-Installation Setup

### 1. Generate SECRET_KEY
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
Add this to your `.env` file.

### 2. Configure Email
Choose an email provider:

#### Option A: Gmail
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-specific-password
EMAIL_FROM=your-email@gmail.com
```

#### Option B: SendGrid
```env
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USERNAME=apikey
EMAIL_PASSWORD=your-sendgrid-api-key
EMAIL_FROM=noreply@yourdomain.com
```

### 3. Database Setup

#### SQLite (Development)
```env
DATABASE_URL=sqlite:///./invoices.db
```

#### PostgreSQL (Production)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/invoice_db
```

### 4. Test Installation
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Run tests
pytest

# Start server
uvicorn app.main:app --reload

# Open browser
# http://localhost:8000/docs
```

---

## ✅ Verify Installation

### Check API Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Access Documentation
Open in browser:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🐛 Troubleshooting

### Python Version Issues
```bash
# Check Python version
python --version
python3 --version

# Use specific version
python3.11 -m venv venv
```

### WeasyPrint Installation Issues

**Linux:**
```bash
# Install missing libraries
sudo apt install -y libpangocairo-1.0-0
```

**macOS:**
```bash
brew install cairo pango
```

**Windows:**
- WeasyPrint should work out of the box
- If issues persist, use GTK installer

### Database Connection Issues
```bash
# Reset database
rm invoices.db
python -c "from app.database import init_db; init_db()"
```

### Port Already in Use
```bash
# Change port
uvicorn app.main:app --port 8001

# Or kill existing process
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

## 🔄 Updating

### Pull Latest Changes
```bash
git pull origin main
```

### Update Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Run Migrations
```bash
alembic upgrade head
```

### Restart Server
```bash
# Stop current server (Ctrl+C)
# Start again
uvicorn app.main:app --reload
```

---

## 🗑️ Uninstallation

### Remove Application
```bash
# Deactivate virtual environment
deactivate

# Remove directory
cd ..
rm -rf invoice-api
```

### Remove Docker Containers
```bash
docker-compose down -v
docker rmi invoice-api:latest
```

---

## 📚 Additional Resources

- **Python Installation:** https://www.python.org/downloads/
- **Docker Installation:** https://docs.docker.com/get-docker/
- **Git Installation:** https://git-scm.com/downloads
- **Virtual Environments:** https://docs.python.org/3/library/venv.html

---

## 💬 Need Help?

- **Documentation:** [Full Docs](/docs)
- **GitHub Issues:** https://github.com/yourusername/invoice-api/issues
- **Email:** support@yourdomain.com
- **Discord:** [Join our community]

---

**Installation complete! 🎉 Ready to create invoices!**