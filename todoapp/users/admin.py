from django.contrib import admin

from users.models import CustomUser
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "is_staff", "date_joined")
    list_filter = ("is_staff", "date_joined")

admin.site.register(CustomUser, UserAdmin)
