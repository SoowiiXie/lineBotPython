from django.contrib import admin

# Register your models here.
from PythyAPI.models import users,teamUp

class usersAdmin(admin.ModelAdmin):
    list_display=('uid','question','state','created_time')
admin.site.register(users, usersAdmin)

class teamUpAdmin(admin.ModelAdmin):
    list_display=('bid','place','amount','timein')
admin.site.register(teamUp, teamUpAdmin)