from django.contrib import admin

# Register your models here.
from PythyAPI.models import users

class usersAdmin(admin.ModelAdmin):
    list_display=('uid','question')
admin.site.register(users, usersAdmin)
