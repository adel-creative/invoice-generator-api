# 🤝 Contributing to Invoice Generator API

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)

---

## 📜 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Keep discussions professional

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Git
- Basic understanding of FastAPI
- Familiarity with REST APIs

### Areas to Contribute

- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🧪 Test coverage
- 🎨 UI/UX improvements
- 🌐 Translations
- 📊 Performance optimizations

---

## 💻 Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/invoice-api.git
cd invoice-api
```

### 2. Set Up Environment

```bash
# Run setup script
chmod +x setup.sh
./setup.sh

# Or manually:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
python -c "from app.database import init_db; init_db()"
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

---

## 🎯 How to Contribute

### Reporting Bugs

**Before submitting:**
- Check existing issues
- Verify it's reproducible
- Collect relevant information

**Bug Report Template:**
```markdown
**Description:** Clear description of the bug

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:** What should happen

**Actual Behavior:** What actually happens

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.11.4]
- API Version: [e.g., 1.0.0]

**Additional Context:** Logs, screenshots, etc.
```

### Suggesting Features

**Feature Request Template:**
```markdown
**Feature Description:** What feature do you want?

**Problem It Solves:** Why is this needed?

**Proposed Solution:** How would it work?

**Alternatives Considered:** Other approaches?

**Additional Context:** Mockups, examples, etc.
```

### Contributing Code

1. **Pick an Issue**
   - Look for issues labeled `good first issue` or `help wanted`
   - Comment on the issue to claim it

2. **Write Code**
   - Follow coding standards (see below)
   - Add tests for new features
   - Update documentation

3. **Test Your Changes**
   ```bash
   make test
   make lint
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub

---

## 📐 Coding Standards

### Python Style

We follow **PEP 8** with some modifications:

```python
# Good
def generate_invoice(
    client_name: str,
    items: List[InvoiceItem],
    currency: str = "USD"
) -> Invoice:
    """
    Generate new invoice.
    
    Args:
        client_name: Client's full name
        items: List of invoice items
        currency: Currency code (default: USD)
        
    Returns:
        Created invoice object
    """
    pass

# Bad
def gen_inv(name,items,curr="USD"):
    pass
```

### Code Formatting

```bash
# Format code
black app tests
isort app tests

# Check formatting
black --check app tests
```

### Type Hints

Always use type hints:

```python
# Good
def calculate_total(items: List[dict]) -> float:
    return sum(item["price"] for item in items)

# Bad
def calculate_total(items):
    return sum(item["price"] for item in items)
```

### Documentation

All functions must have docstrings:

```python
def send_email(to: str, subject: str, body: str) -> bool:
    """
    Send email to recipient.
    
    Args:
        to: Recipient email address
        subject: Email subject line
        body: Email body content
        
    Returns:
        True if sent successfully, False otherwise
        
    Raises:
        EmailError: If email sending fails
    """
    pass
```

---

## 🧪 Testing

### Writing Tests

```python
def test_create_invoice():
    """Test invoice creation with valid data"""
    response = client.post("/invoices/generate", json={...})
    assert response.status_code == 201
    assert "invoice_number" in response.json()
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_invoices.py

# With coverage
pytest --cov=app

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

### Test Coverage

Aim for **80%+ coverage** on new code.

```bash
# Generate coverage report
pytest --cov=app --cov-report=html
# Open htmlcov/index.html
```

---

## 🔄 Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
How was this tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests pass

## Screenshots (if applicable)
Add screenshots here
```

### Review Process

1. **Automated Checks**
   - Tests must pass
   - Linting must pass
   - Coverage maintained

2. **Code Review**
   - At least 1 approval required
   - Address all feedback

3. **Merge**
   - Squash commits
   - Update changelog
   - Deploy to staging

---

## 📝 Commit Message Guidelines

Follow **Conventional Commits**:

```
feat: add email sending feature
fix: resolve PDF generation bug
docs: update API documentation
test: add invoice creation tests
refactor: simplify authentication logic
style: format code with black
perf: optimize database queries
chore: update dependencies
```

### Examples

```bash
# Good
git commit -m "feat: add support for EUR currency"
git commit -m "fix: resolve QR code generation issue #123"
git commit -m "docs: add deployment guide"

# Bad
git commit -m "updated stuff"
git commit -m "fixes"
git commit -m "wip"
```

---

## 🏗️ Project Structure

```
app/
├── api/           # API endpoints
├── models/        # Database models
├── schemas/       # Pydantic schemas
├── services/      # Business logic
├── templates/     # Invoice templates
└── utils/         # Helper functions
```

### Adding New Endpoints

1. Create route in `app/api/`
2. Add schemas in `app/schemas/`
3. Implement logic in `app/services/`
4. Add tests in `tests/`
5. Update documentation

---

## 🌐 Internationalization

### Adding New Language

1. Create template in `app/templates/invoice_{lang}.html`
2. Update `LanguageEnum` in schemas
3. Add translation dictionary
4. Update documentation

---

## 🐛 Debugging

### Enable Debug Mode

```python
# .env
DEBUG=true
```

### View Logs

```bash
# Application logs
tail -f app.log

# Docker logs
docker-compose logs -f
```

### Common Issues

**Issue:** Import errors
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

**Issue:** Database errors
```bash
# Solution: Reset database
make db-reset
```

---

## 📚 Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com
- **SQLAlchemy:** https://docs.sqlalchemy.org
- **Pydantic:** https://docs.pydantic.dev
- **WeasyPrint:** https://doc.courtbouillon.org/weasyprint/

---

## 💬 Getting Help

- **GitHub Issues:** For bugs and features
- **Discussions:** For questions and ideas
- **Email:** support@yourdomain.com
- **Discord:** [Join our community]

---

## 🎉 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in documentation

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing! 🙏**

Every contribution, no matter how small, makes a difference!