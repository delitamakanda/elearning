from django.contrib import admin
from agenda.models import Event
from agenda.models import EventGuest
from agenda.models import Circle
from agenda.models import UserInfo
from agenda.models import Contact
from agenda.models import Invitation

from agenda.models import Post
from agenda.models import Comment

# Register your models here.
admin.site.register(Event)
admin.site.register(EventGuest)
admin.site.register(Circle)
admin.site.register(UserInfo)
admin.site.register(Contact)
admin.site.register(Invitation)

class PostAdmin(admin.ModelAdmin):
    list_display = ['title',]
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
