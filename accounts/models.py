from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin

class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def _create_user(self, email, password, first_name=None, last_name=None, is_active=True, is_staff=False, is_admin=False, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, firstName=first_name, lastName=last_name)
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.is_superuser = extra_fields.get('is_superuser', False)
        user.is_active = is_active
        user.save()
        return user

    def create_user(self, email, password = None, first_name=None, last_name=None, is_active=True, is_staff=False, is_admin=False, **extra_fields):
        user_obj =self.model.objects.filter(email=email)

        if(user_obj.exists() and not None):
            return user_obj[0]

        return self._create_user(email, password = password, first_name=first_name, last_name=last_name, is_active=is_active, is_staff=is_staff, is_admin=is_admin, **extra_fields)

    def create_staffuser(self, email, first_name=None, last_name=None, password=None):
        user = self.create_user(
                email,
                password=password,
                first_name = first_name,
                last_name = last_name,
                is_staff=True
        )
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    email       = models.EmailField(verbose_name='email address', max_length=255, unique = True, null = True)
    is_active   = models.BooleanField(verbose_name='active', default=True)
    staff       = models.BooleanField(verbose_name= 'staff status', default = False)
    admin       = models.BooleanField(verbose_name= 'admin status', default = False)
    firstName   = models.CharField(max_length=32, default='', null=True, blank=True)
    lastName    = models.CharField(max_length=32, default='', null=True, blank=True)
    longitude = models.DecimalField(decimal_places=55, max_digits=60, null = True, blank = True)
    latitude = models.DecimalField(decimal_places=55, max_digits=60, null=True, blank = True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone       = models.CharField(validators=[phone_regex],max_length = 15, null=True, blank = True)

    STATUS_CHOICE = (
        (0, "Free"),
        (1, "Chill"),
        (2, "Away"),
        (3, "Busy"),
        (4, "Hidden"),
        (5, "Sleeping"),
    )
    status      = models.IntegerField(choices = STATUS_CHOICE, default = 0)


    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    @property
    def is_staff(self):
        if self.admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin
