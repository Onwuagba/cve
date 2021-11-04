from django.contrib import admin
from django.contrib.postgres import fields
from .models import HouseInfo, Payment, User, UserHouse

# Register your models here.

@admin.register(User)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'user_role', 'regToken')

# class UserAdmin(admin.ModelAdmin):
#     fields = ('first_name', 'last_name', 'phone_number', 'user_role')

# admin.site.register (User)
# fields = ('first_name', 'last_name', 'phone_number', 'user_role')
admin.site.register (HouseInfo)
admin.site.register (UserHouse)
admin.site.register (Payment)