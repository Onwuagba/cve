from django.contrib import admin
from .models import HouseInfo, Payment, User, UserHouse, ProjectUpdate, Feature

# Register your models here.

@admin.register(User)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'user_role', 'regToken')

class HouseAdmin(admin.ModelAdmin):
    list_display = ('title', 'quantity', 'cost', 'desription', 'images', 'date_created', 'date_updated', 'created_by' )
admin.site.register (HouseInfo, HouseAdmin)


admin.site.register (UserHouse)
admin.site.register (Payment)
admin.site.register (ProjectUpdate)
admin.site.register (Feature)