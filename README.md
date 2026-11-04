# my-elearning

A Django 6-based e-learning platform built for Python 3.13.

[![Django CI](https://github.com/delitamakanda/elearning/actions/workflows/django.yml/badge.svg?branch=master)](https://github.com/delitamakanda/elearning/actions/workflows/django.yml)

## Features
- Create and organize courses with modules and lessons
- Students can enroll and track their progress
- Background task processing with Celery
- Full-text search across courses

## Getting Started

### Installation
```bash
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

### Run the project
```bash
python manage.py runserver
celery -A myelearning worker -l info -B
```

## Running Tests
```bash
python manage.py test
```

## Demo data
```bash
python manage.py seed_demo   # DEBUG only — demo-teacher / demo-student, password demo-password-123
```

## Agentic workflow
Issues are specs: a Claude agent refines them, implements one ticket at a time and opens a PR for human review. See [docs/agentic-workflow.md](docs/agentic-workflow.md).

## TODO
- [ ] Nice layout
- [ ] Login via Google
- [x] API
- [x] Celery worker
- [x] Reset Password
- [x] Search Form

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

