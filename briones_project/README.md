# Briones Portfolio Project

A Django-based personal portfolio website showcasing projects, skills, education, and professional information.

## Features

- **Personal Profile**: Display name, tagline, and profile photo
- **About Section**: Detailed bio and career goals
- **Projects Gallery**: Showcase of personal and professional projects with links
- **Skills Display**: Categorized skills with proficiency levels
- **Education Timeline**: Academic background and qualifications
- **Contact Form**: Visitor messaging system with status tracking
- **Admin Panel**: Django admin for content management

## Project Structure

```
briones_project/
├── manage.py                 # Django management script
├── db.sqlite3              # SQLite database
├── briones_project/        # Main Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── briones_app/            # Main application
│   ├── models.py           # Database models (Profile, Project, Skill, etc.)
│   ├── views.py            # View functions
│   ├── urls.py             # App URL patterns
│   ├── forms.py            # Contact form
│   ├── admin.py            # Django admin configuration
│   ├── templates/          # HTML templates
│   ├── static/             # CSS, JS, images
│   └── migrations/         # Database migrations
├── media/                  # User-uploaded media
└── staticfiles/            # Collected static files
```

## Models Overview

### Core Models
- **Profile**: Personal information (singleton)
- **About**: Bio and career goals (singleton)
- **ContactInfo**: Public contact details (singleton)
- **ContactMessage**: Incoming form submissions
- **Project**: Portfolio projects with links and images
- **Skill**: Technical skills with categories and proficiency
- **Education**: Academic background
- **Owner**: Site owner information (singleton)

## Technology Stack

- **Backend**: Django 6.0.3
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Static Files**: Django's staticfiles system
- **Email**: Console backend (development)

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd briones_project
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser for admin access**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

   **Requirements**
   ```
   asgiref==3.11.1
   Django==5.2.12
   dotenv==0.9.9
   pillow==12.1.1
   python-dotenv==1.2.2
   sqlparse==0.5.5
   tzdata==2025.3

   ```

8. **Access the application**
   - Website: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## Content Management

### Using the Admin Panel
1. Log in with your superuser credentials
2. Navigate to the respective sections:
   - **Profile**: Add your name, tagline, and photo
   - **About**: Write your bio and career goals
   - **Contact Info**: Set up email and social links
   - **Projects**: Add portfolio projects
   - **Skills**: List technical skills with proficiency
   - **Education**: Add academic background

### Important Notes
- Profile, About, ContactInfo, and Owner models are singletons (only one record allowed)
- Projects and Skills support ordering for display priority
- Contact messages can be managed through the admin panel

## Development

### Adding New Features
1. Define models in `briones_app/models.py`
2. Create migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`
4. Add admin configuration in `briones_app/admin.py`
5. Create views and templates as needed

### Customization
- Templates are located in `briones_app/templates/briones_app/`
- Static files (CSS, JS, images) in `briones_app/static/`
- User uploads stored in `media/`

## Deployment Considerations

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure proper `ALLOWED_HOSTS`
3. Set up a production database (PostgreSQL recommended)
4. Configure static files serving
5. Set up proper email backend
6. Use environment variables for sensitive data

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For questions or support, please use the contact form on the website or create an issue in the project repository.
