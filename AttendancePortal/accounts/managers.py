from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, unique_id, first_name, last_name,password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not unique_id:
            raise ValueError('Users must have an email address')

        user = self.model(
            unique_id = unique_id,
            first_name = first_name,
            last_name = last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, unique_id, first_name, last_name,password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            unique_id=unique_id,
            password=password,
            first_name = first_name,
            last_name= last_name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
