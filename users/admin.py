from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name')


