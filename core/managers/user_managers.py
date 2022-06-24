from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, rut, name, lastname, email, role, profession, birth_date, password=None):
        if not rut:
            raise ValueError('The user most have a rut.')

        email = self.normalize_email(email)
        user = self.model(rut=rut, email=email, name=name, profession=profession,
                          lastname=lastname, role=role, birth_date=birth_date)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, rut, name, lastname, email, role, birth_date, profession=None, password=None):
        if not rut:
            raise ValueError('The user most have a rut.')
        email = self.normalize_email(email)
        user = self.model(rut=rut, email=email, name=name, profession=profession,
                          lastname=lastname, role=role, birth_date=birth_date)
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self.db)
        return user
