from django.contrib import admin
from students.models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User

admin.site.register(User, UserAdmin)
