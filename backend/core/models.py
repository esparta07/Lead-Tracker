from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, role=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')

        user = self.model(phone_number=phone_number, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        # Create and save a new superuser with the given phone number and password
        user = self.create_user(phone_number, password, **extra_fields)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    ADMIN = 1
    USER = 2

    ROLE_CHOICES = (
        (ADMIN, 'ADMIN'),
        (USER, 'USER'),
    )
    user_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50,unique=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    USER_CHOICES = (
        ('BD', 'BD'),
        ('DM', 'DM'),
        ('Admin', 'Admin'),
    )
    full_name = models.CharField(max_length=50,blank=True)
    email = models.EmailField(max_length=100, unique=False, default="")
    user_type =models.CharField(max_length=40, choices=USER_CHOICES, blank=True)
    
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    objects = UserManager()

    def __str__(self):
        return str(self.full_name) if self.full_name else self.phone_number

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_role(self):
        if self.role == 1:
            user_role = 'ADMIN'
        elif self.role == 2:
            user_role = 'USER'
        return user_role
    


