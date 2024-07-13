from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from tenant.models import TenantAwareModel

from .managers import CustomUserManager


class CustomUser(AbstractUser, TenantAwareModel):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(null=True, max_length=255)
    last_name = models.CharField(null=True, max_length=255)

    is_company_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# class UserModel(TenantAwareModel):
#     first_name = models.CharField(verbose_name="First Name", max_length=255)
#     last_name = models.CharField(verbose_name="Last Name", max_length=255)
#     email = models.EmailField(verbose_name="Email", unique=True)
#     password = models.CharField(verbose_name="Password", max_length=255)
#     is_company_admin = models.BooleanField(default=False)

#     @property
#     def full_name(self):
#         return f"{self.first_name} {self.last_name}"

#     @property
#     def get_tenant(self):
#         return f"{self.tenant}"

#     def save(self, *args, **kwargs):
#         try:
#             if not self.pk:
#                 self.password = hash_password(self.password)
#             else:
#                 existing_user = UserModel.objects.get(pk=self.pk)
#                 if self.password != existing_user.password:
#                     self.password = hash_password(self.password)

#         except UserModel.DoesNotExist:
#             pass

#         except Exception as e:
#             ic(f"An error occurred while saving UserModel: {e}")
#             raise

#         return super().save(*args, **kwargs)


# def authenticate_user(email: str, password: str, tenant: TenantAwareModel) -> bool:
#     try:
#         user = UserModel.objects.get(email=email, tenant=tenant)
#         return check_password(password=password, hashed=user.password)

#     except UserModel.DoesNotExist as e:
#         return False

#     except Exception as e:
#         ic(e)
#         raise Exception(f"Exception Occoured {e}")


# def hash_password(password: str) -> str:
#     salt = bcrypt.gensalt()
#     hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
#     return hashed.decode("utf-8")


# def check_password(password: str, hashed: str) -> bool:
#     return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
