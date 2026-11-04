from io import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.courses.management.commands.seed_demo import DEMO_PASSWORD
from apps.courses.models import Course, Module


@override_settings(DEBUG=True)
class SeedDemoCommandTests(TestCase):
    """Les données de démo servent au développement local et aux agents."""

    def seed(self):
        call_command("seed_demo", stdout=StringIO())

    def test_seed_is_idempotent(self):
        self.seed()
        counts = (Course.objects.count(), Module.objects.count())
        self.seed()
        self.assertEqual((Course.objects.count(), Module.objects.count()), counts)
        self.assertGreater(counts[0], 0)

    def test_teacher_can_open_dashboard(self):
        self.seed()
        self.assertTrue(
            self.client.login(username="demo-teacher", password=DEMO_PASSWORD)
        )
        response = self.client.get(reverse("courses:manage_course_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django for beginners")

    def test_student_can_open_quiz_list(self):
        self.seed()
        self.assertTrue(
            self.client.login(username="demo-student", password=DEMO_PASSWORD)
        )
        response = self.client.get(reverse("students:student_quiz_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python basics")

    @override_settings(DEBUG=False)
    def test_refuses_to_run_without_debug(self):
        with self.assertRaises(CommandError):
            self.seed()
