from django.contrib.auth.models import (
    BaseUserManager
)


# TODO здесь должен быть менеджер для модели Юзера.
# TODO Поищите эту информацию в рекомендациях к проекту
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, first_name, last_name, phone,
                    password, **extra_fields):
        # values = [email, phone]
        # field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        # for field_name, value in field_value_map.items():
        #     if not value:
        #         raise ValueError('The {} value must be set'.format(field_name))

        # extra_fields.setdefault('is_staff', False)
        # extra_fields.setdefault('is_superuser', False)

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role='user',
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # def _create_user(self, email, phone, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', False)
    #     extra_fields.setdefault('is_superuser', False)
    #     return self._create_user(email, phone, password, **extra_fields)

    def create_superuser(self, email, first_name, last_name, phone,
                         password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # if extra_fields.get('is_staff') is not True:
        #     raise ValueError('Superuser must have is_staff=True.')
        # if extra_fields.get('is_superuser') is not True:
        #     raise ValueError('Superuser must have is_superuser=True.')

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role='admin',
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
