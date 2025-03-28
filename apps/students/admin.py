from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.students.models import (User, Quiz, Question, Answer, Student, TakenQuiz, Profile, StudentAnswer, Tag)
from apps.common.paginator import DumbPaginator, TimeLimitedPaginator

class TagAdmin(admin.ModelAdmin):
    model = Tag


class StudentAnswerAdmin(admin.ModelAdmin):
    paginator = TimeLimitedPaginator
    model = StudentAnswer

class AnswerInline(admin.StackedInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(admin.ModelAdmin):
    paginator = TimeLimitedPaginator
    inlines = (ProfileInline,)
    model = User
    list_display = ['username', 'email']
    list_filter = ['is_teacher', 'is_student', 'is_staff']

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Student)
admin.site.register(TakenQuiz)
admin.site.register(StudentAnswer, StudentAnswerAdmin)
admin.site.register(Tag, TagAdmin)
# admin.site.register(Profile)
