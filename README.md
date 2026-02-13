cat > README.md << 'EOF'

# My Services Django Website

A comprehensive Django-based services website with blog, contact form, and admin panel.

## Features

- Service listings with categories
- Blog with comments
- Contact form
- Admin dashboard
- Responsive design

## Installation

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install requirements: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Run server: `python manage.py runserver`

## Usage

Visit http://localhost:8000 to see the site
Admin panel: http://localhost:8000/admin
EOF

git add README.md
git commit -m "Add README"
git push
