# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-02

### 🎉 Initial Release - MVP

#### Added
- **Authentication System**
  - JWT-based authentication
  - User registration and login
  - Password hashing with bcrypt
  - Unique payment links per user

- **Invoice Management**
  - Create invoices with multiple items
  - Bilingual PDF generation (Arabic RTL & English LTR)
  - QR code generation for payments
  - Invoice CRUD operations
  - Invoice status tracking (draft, sent, paid, cancelled)

- **Email Service**
  - Send invoices via email
  - HTML email templates
  - PDF attachments
  - Rate limiting (5 emails/hour per user)

- **Multi-language Support**
  - Arabic (RTL) invoice templates
  - English (LTR) invoice templates
  - Professional modern design

- **Multi-currency Support**
  - MAD (Moroccan Dirham)
  - USD (US Dollar)
  - EUR (Euro)
  - SAR (Saudi Riyal)
  - AED (UAE Dirham)

- **API Features**
  - RESTful API design
  - Automatic OpenAPI documentation
  - RapidAPI ready
  - 14 endpoints total

- **User Management**
  - User profiles
  - Company information
  - Statistics dashboard
  - Payment link management

- **Documentation**
  - Complete API documentation
  - Quick start guide
  - Deployment guide
  - Contributing guidelines
  - Postman collection

- **DevOps**
  - Docker support
  - Docker Compose configuration
  - GitHub Actions CI/CD
  - Database migrations (Alembic)
  - Makefile commands
  - Setup script

- **Testing**
  - Unit tests for authentication
  - Integration tests for invoices
  - Service tests
  - pytest configuration
  - Coverage reporting

### Technical Details
- FastAPI 0.109.0
- Python 3.11+
- SQLAlchemy ORM
- WeasyPrint for PDF
- Jinja2 for templates
- JWT authentication
- Async email sending

### Security
- JWT token authentication
- Password hashing (bcrypt)
- Input validation (Pydantic)
- CORS protection
- SQL injection prevention
- Rate limiting on email
- Environment variable protection

### Known Limitations
- SQLite database (MVP - PostgreSQL recommended for production)
- Email rate limiting (5/hour per user)
- No payment gateway integration yet (coming in v1.1)
- Basic error handling (will be enhanced)

---

## [Unreleased]

### Planned for v1.1.0
- [ ] Stripe payment integration
- [ ] PayPal support
- [ ] Webhook notifications
- [ ] Enhanced error messages
- [ ] More currency options
- [ ] Invoice templates marketplace

### Planned for v1.2.0
- [ ] Recurring invoices
- [ ] Invoice reminders
- [ ] Multi-user teams
- [ ] Advanced analytics
- [ ] Custom branding

### Planned for v2.0.0
- [ ] Mobile SDK (React Native)
- [ ] White-label solution
- [ ] Accounting software integrations
- [ ] AI-powered features
- [ ] Advanced reporting

---

## Version History

### [1.0.0] - 2025-10-02
- Initial MVP release
- Full feature set as documented above

---

## Migration Guide

### From Development to v1.0.0
No migration needed - this is the first release.

### Future Migrations
Migration guides will be provided with each major version.

---

## Contributors

- **Lead Developer:** [Your Name]
- **Contributors:** See [CONTRIBUTORS.md](CONTRIBUTORS.md)

---

## Support

For issues, questions, or feature requests:
- GitHub Issues: https://github.com/yourusername/invoice-api/issues
- Email: support@yourdomain.com
- Documentation: https://docs.yourdomain.com

---

**Thank you for using Invoice Generator API! 🎉**