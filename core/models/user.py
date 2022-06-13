import datetime
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, rut, name, lastname, email, role, profession, birthday, birth_month, birth_year, password=None):
        if not rut:
            raise ValueError('The user most have a rut.')

        email = self.normalize_email(email)
        birth_date = datetime.date(birth_year, birth_month, birthday)
        user = self.model(rut=rut, email=email, name=name, profession=profession,
                          lastname=lastname, role=role, birth_date=birth_date)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, rut, name, lastname, email, role, profession, birthday, birth_month, birth_year, password=None):
        user = self.create_user(rut, name, lastname, email, role,
                                profession, birthday, birth_month, birth_year, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    role = models.IntegerField()
    birth_date = models.DateField()
    profession = models.CharField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'lastname', 'rut', 'role', 'birth_date']

    class Meta:
        managed = True
        app_label = 'core'