from django.db import models
from django .contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

# Create your models here.
class CustomAccountManager(BaseUserManager):

    def create_user(self,email,user_name,first_name,last_name,password,**other_fields):
        if not email:
            raise ValueError('Your email address is required')
        email=self.normalize_email(email)
        email=email.strip().lower()
        print(email)
        user = self.model(email=email,user_name=user_name,first_name=first_name,last_name=last_name,**other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,user_name,first_name,last_name,password,**other_fields):

        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned ti is_staff=True.')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned ti is_superuser=True.')

        return self.create_user(email,user_name,first_name,last_name,password,**other_fields)




class AccountsUser(AbstractBaseUser,PermissionsMixin):
    email =models.EmailField(unique=True)
    sap_no =models.PositiveIntegerField()
    user_name =models.CharField(max_length=20)
    first_name =models.CharField(max_length=50,blank=True)
    last_name =models.CharField(max_length=50,blank=True)
    is_active =models.BooleanField(default=False)
    is_staff =models.BooleanField(default=False)
    created_on =models.DateTimeField(auto_now_add=True)

    objects = CustomAccountManager()

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['user_name','sap_no','first_name','last_name']

    def _str_(self):
        return self.email