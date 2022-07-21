import csv
import datetime

from django.http import HttpResponse
from django.contrib import admin
from courses.models import Subject
from courses.models import Course
from courses.models import Module
from courses.models import Review
from courses.models import BadgeAward
from django.utils.translation import gettext_lazy as _
from common.paginator import TimeLimitedPaginator, DumbPaginator

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; \
            filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    paginator = TimeLimitedPaginator
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    inlines = [ModuleInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    paginator = DumbPaginator
    list_display = ['course', 'rating', 'user_name', 'comment', 'pub_date']
    list_filter = ['pub_date', 'user_name']
    search_fields = ['comment']
    actions = [export_to_csv]


admin.site.register(BadgeAward)
