from django.contrib import admin
from courses.models import Subject
from courses.models import Course
from courses.models import Module
from courses.models import Review
from django.utils.translation import gettext_lazy as _


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['course', 'rating', 'user_name', 'comment', 'pub_date']
    list_filter = ['pub_date', 'user_name']
    search_fields = ['comment']
