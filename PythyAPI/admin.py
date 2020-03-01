from django.contrib import admin

# Register your models here.
from PythyAPI.models import users

class usersAdmin(admin.ModelAdmin):
    list_display=('uid','question','state')
admin.site.register(users, usersAdmin)
