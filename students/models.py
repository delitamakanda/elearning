from django.contrib.auth.models import AbstractUser
from django.db import models
from courses.models import Subject
from courses.models import Quiz


# Create your models here.
# class Role(models.Model):
  # """
  # The Role entries are managed by the system,
  # automatically created via a Django data migration.
  # """
  # STUDENT = 1
  # TEACHER = 2
  # ADMIN = 3
  # ROLE_CHOICES = (
      # (STUDENT, 'student'),
      # (TEACHER, 'teacher'),
      # (ADMIN, 'admin'),
  # )

  # id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)
  
   # def __str__(self):
      # return self.get_id_display()
  
# class User(AbstractUser):
  # roles = models.ManyToManyField(Role)
  
  
class User(AbstractUser):
  is_student = models.BooleanField(default=False)
  is_teacher = models.BooleanField(default=False)


class Student(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
  interests = models.ManyToManyField(Subject, related_name='interested_students')
