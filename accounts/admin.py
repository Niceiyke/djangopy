from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from.models import AccountsUser


# Register your models here.
class UserAdminConfig(UserAdmin):
    search_fields =('email','user_name','sap_no','first_name','last_name')
    list_filter=('email','user_name','first_name','is_active','is_staff')
    ordering=('-created_on',)
    list_display= ('email','user_name','sap_no','first_name','last_name','is_active','is_staff',)
    fieldsets = (
        (None, {
            "fields": (
                'email','sap_no','user_name','first_name','last_name','password'
            ),
        }),
        ('Permissions',{
            'fields':('is_staff','is_active','groups')
        }),
    )

    add_fieldsets = (
        (
        None, {
                'classes':('wide',),
                'fields':('email','sap_no','user_name','first_name','last_name','password1','password2','is_active','is_staff',)
            }
        ),
    )

    
    



admin.site.register(AccountsUser,UserAdminConfig)
