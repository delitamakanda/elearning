from django.contrib import admin
from students.models import User
from students.models import Quiz
from students.models import Question
from students.models import Answer
from students.models import Student
from students.models import TakenQuiz
from students.models import StudentAnswer

class AnswerInline(admin.StackedInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

# Register your models here.
admin.site.register(User)
admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Student)
admin.site.register(TakenQuiz)
admin.site.register(StudentAnswer)
