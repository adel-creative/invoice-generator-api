#!/bin/bash

# Invoice Generator API - Quick Setup Script
# This script sets up the development environment

echo "🚀 Invoice Generator API - Quick Setup"
echo "========================================"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo -e "\n${YELLOW}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python $python_version found${NC}"

# Create virtual environment
echo -e "\n${YELLOW}Creating virtual environment...${NC}"
python3 -m venv venv
echo -e "${GREEN}✓ Virtual environment created${NC}"

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Upgrade pip
echo -e "\n${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ pip upgraded${NC}"

# Install dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Copy environment file
echo -e "\n${YELLOW}Setting up environment variables...${NC}"
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}⚠ Please edit .env with your settings${NC}"
else
    echo -e "${YELLOW}⚠ .env already exists, skipping${NC}"
fi

# Create directories
echo -e "\n${YELLOW}Creating directories...${NC}"
mkdir -p static/invoices
mkdir -p static/qr_codes
mkdir -p alembic/versions
echo -e "${GREEN}✓ Directories created${NC}"

# Initialize database
echo -e "\n${YELLOW}Initializing database...${NC}"
python -c "from app.database import init_db; init_db()"
echo -e "${GREEN}✓ Database initialized${NC}"

# Generate secret key
echo -e "\n${YELLOW}Generating SECRET_KEY...${NC}"
secret_key=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
echo -e "${GREEN}✓ SECRET_KEY generated${NC}"
echo -e "${YELLOW}Add this to your .env file:${NC}"
echo -e "${GREEN}SECRET_KEY=$secret_key${NC}"

# Setup complete
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"

echo -e "\n${YELLOW}Next steps:${NC}"
echo "1. Edit .env file with your settings (especially EMAIL credentials)"
echo "2. Add the SECRET_KEY above to your .env"
echo "3. Run: uvicorn app.main:app --reload"
echo "4. Open: http://localhost:8000/docs"

echo -e "\n${YELLOW}Quick commands:${NC}"
echo "  make run       - Start development server"
echo "  make test      - Run tests"
echo "  make help      - Show all available commands"

echo -e "\n${GREEN}Happy coding! 🎉${NC}"