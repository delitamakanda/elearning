# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo          # demo data (DEBUG only): demo-teacher / demo-student, password demo-password-123
python manage.py runserver          # http://localhost:8000/course/
python manage.py check
python manage.py test               # Django test runner (unittest-style TestCase)
python manage.py test apps.courses.tests.SeedDemoCommandTests   # a single test class
celery -A myelearning worker -l info -B   # background tasks (needs Redis)
```

Without `DATABASE_URL` the app uses SQLite (`db.sqlite3`); without `REDIS_URL` the cache is a dummy cache. E-mails go to the console. `docker compose up` runs Postgres + Redis + web + worker (`.env.docker`).

Lint/format: Ruff (config in `pyproject.toml`). The codebase is **not** clean yet (~150 Ruff errors, many unformatted files), so only lint what you touch: `bash scripts/agent/lint-changed.sh --fix` then `--check` (compares to `origin/master`). Do not reformat untouched files.

## Architecture

Django 6, Python 3.13. Project package `myelearning/` (settings, URLs, Celery app, S3 storage backends for production via `settings_production.py`). Apps live in `apps/`:

- `apps/courses/` — subjects, courses, modules and polymorphic module contents (`Content` with a `GenericForeignKey` to `Text` / `File` / `Image` / `Video`, all inheriting `ItemBase`), reviews, badges, search, Celery tasks (`tasks.py`), custom `OrderField` (`fields.py`). Teacher management views use `braces` mixins (`OwnerCourseMixin`, `OwnerCourseEditMixin`) with model permissions `courses.add_course` etc. The DRF API is in `apps/courses/api/` (mounted at `/api/`, default permission `IsAuthenticatedOrReadOnly`).
- `apps/students/` — custom user model `students.User` (`AUTH_USER_MODEL`, flags `is_student` / `is_teacher`), `Profile` (created by a `post_save` signal), `Student` (created by the student sign-up form, holds quiz interests), quizzes (`Quiz`, `Question`, `Answer`, `TakenQuiz`, `StudentAnswer`). Views are split in `views/classroom.py`, `views/students.py`, `views/teachers.py`; use the `student_required` / `teacher_required` decorators. Login also works with the e-mail address (`authentication.EmailAuthBackend`).
- `apps/common/` — shared paginator and serializers.

Templates are project-level in `templates/` (Bootstrap 4, `django-crispy-forms`, `widget_tweaks`); static files in `static/`, served by WhiteNoise.

### Known issues

- **Migration drift**: `DEFAULT_AUTO_FIELD` is `BigAutoField` but every existing migration uses `AutoField`, and the `owner` field of `Text`/`File`/`Image`/`Video` differs from its migration. `makemigrations --check` therefore fails on `master`. When you change a model, keep only the operations related to your change in the new migration, unless the ticket is about fixing this drift.
- `QuizListView` returns the user instead of a queryset when the logged-in user has no `Student` record.

## Conventions

- Business logic in models, managers or small service functions — not in templates, and keep views thin.
- Critical multi-step writes in `transaction.atomic()`; watch for N+1 queries (`select_related` / `prefetch_related`).
- Every view that changes data requires authentication and checks ownership / role (`OwnerMixin`, permissions, `student_required` / `teacher_required`). Keep CSRF protection.
- New models or fields come with a migration (`python manage.py makemigrations <app> --name <explicit_name>`); never edit existing migrations.
- DRF serializers stay strict (explicit `fields`, validation) and endpoints declare their permissions.
- New tests go in the app (`tests.py` or a `tests/` package), using `TestCase`, the test client, and `APIClient` for the API. Commands guarded by `DEBUG` need `@override_settings(DEBUG=True)` (the test runner forces `DEBUG=False`).
- Pages must stay usable on mobile and meet WCAG AA (labels, contrast, focus).

## Agentic workflow

Issues are specs: a Claude agent (GitHub Actions) refines them, implements one ticket at a time and opens a PR for human review. See `docs/agentic-workflow.md`. Agents must never modify `.github/`.
