"""Données de démonstration pour le développement local et les agents.

Crée (ou complète, la commande est idempotente) :
- un compte enseignant `demo-teacher` et un compte élève `demo-student` ;
- quelques matières, cours, modules et contenus texte ;
- un quiz lié au centre d'intérêt de l'élève ;
- l'inscription de l'élève au premier cours et un avis.

À ne lancer que sur une base de développement : les mots de passe sont publics.

    python manage.py seed_demo
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.courses.models import Content, Course, Module, Review, Subject, Text
from apps.students.models import Answer, Question, Quiz, Student, Tag

DEMO_PASSWORD = "demo-password-123"

SUBJECTS = {
    "programming": "Programming",
    "data-science": "Data science",
    "design": "Design",
}

COURSES = [
    (
        "programming",
        "Django for beginners",
        "Build your first web application with Django: models, views and templates.",
        ["Getting started", "Models and the ORM", "Views and templates"],
    ),
    (
        "programming",
        "REST APIs with Django REST framework",
        "Serializers, viewsets and authentication for a clean JSON API.",
        ["Serializers", "Viewsets and routers"],
    ),
    (
        "data-science",
        "Pandas essentials",
        "Load, clean and analyse tabular data with pandas.",
        ["DataFrames", "Grouping and aggregation"],
    ),
    (
        "design",
        "UI design fundamentals",
        "Typography, colour and layout for readable interfaces.",
        ["Typography", "Layout grids"],
    ),
]


class Command(BaseCommand):
    help = "Crée des données de démonstration (comptes, cours, modules, contenus)."

    @transaction.atomic
    def handle(self, *args, **options):
        from django.conf import settings

        if not settings.DEBUG:
            raise CommandError("seed_demo ne s'exécute qu'avec DEBUG=True.")

        teacher = self._user("demo-teacher", is_teacher=True)
        student = self._user("demo-student", is_student=True)
        teacher.user_permissions.add(
            *Permission.objects.filter(
                content_type__app_label="courses",
                codename__in=[
                    f"{action}_{model}"
                    for action in ("add", "change", "delete", "view")
                    for model in ("course", "module", "content")
                ],
            )
        )

        subjects = {
            slug: Subject.objects.get_or_create(slug=slug, defaults={"title": title})[0]
            for slug, title in SUBJECTS.items()
        }
        text_type = ContentType.objects.get_for_model(Text)

        for subject_slug, title, overview, modules in COURSES:
            course, _ = Course.objects.get_or_create(
                title=title,
                defaults={
                    "owner": teacher,
                    "subject": subjects[subject_slug],
                    "overview": overview,
                },
            )
            for module_title in modules:
                module, created = Module.objects.get_or_create(
                    course=course,
                    title=module_title,
                    defaults={"description": f"{module_title} — {title}."},
                )
                if created:
                    text = Text.objects.create(
                        owner=teacher,
                        title=f"Introduction: {module_title}",
                        content=f"Welcome to the “{module_title}” module of {title}.",
                    )
                    Content.objects.create(
                        module=module, content_type=text_type, object_id=text.pk
                    )

        # Comme l'inscription élève (StudentSignUpForm) : fiche Student + centres
        # d'intérêt, et un quiz correspondant pour que la liste ne soit pas vide.
        tag, _ = Tag.objects.get_or_create(name="Python", defaults={"color": "#3572A5"})
        student_profile, _ = Student.objects.get_or_create(user=student)
        student_profile.interests.add(tag)
        quiz, created = Quiz.objects.get_or_create(
            name="Python basics", defaults={"owner": teacher, "tags": tag}
        )
        if created:
            question = Question.objects.create(
                quiz=quiz, text="Which keyword defines a function in Python?"
            )
            Answer.objects.bulk_create(
                [
                    Answer(question=question, text="def", is_correct=True),
                    Answer(question=question, text="func", is_correct=False),
                    Answer(question=question, text="lambda", is_correct=False),
                ]
            )

        first = Course.objects.filter(owner=teacher).order_by("created").first()
        if first:
            first.students.add(student)
            Review.objects.get_or_create(
                course=first,
                user_name=student,
                defaults={"comment": "Clear and well paced.", "rating": 5},
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Données de démo prêtes : {Course.objects.count()} cours. "
                f"Comptes demo-teacher / demo-student, mot de passe « {DEMO_PASSWORD} »."
            )
        )

    def _user(self, username, **flags):
        user, created = get_user_model().objects.get_or_create(
            username=username,
            defaults={"email": f"{username}@example.com", **flags},
        )
        if created:
            user.set_password(DEMO_PASSWORD)
            user.save()
        return user
