# my-elearning

A Django-based e-learning platform built with Python 3.

[![Django CI](https://github.com/delitamakanda/elearning/actions/workflows/django.yml/badge.svg?branch=master)](https://github.com/delitamakanda/elearning/actions/workflows/django.yml)

## Features
- Create and organize courses with modules and lessons
- Students can enroll and track their progress
- Background task processing with Celery
- Full-text search across courses

## Getting Started

### Installation
```bash
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

## TODO
- [ ] Nice layout
- [ ] Login via Google
- [x] API
- [x] Celery worker
- [x] Reset Password
- [x] Search Form

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

