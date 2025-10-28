import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    AGENCY = "AGENCY", "Agency"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', UserRole.ADMIN)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.AGENCY)
    email = models.EmailField(unique=True, blank=False)
    company_name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    contact_details = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    # adding constraint for database sut still return default response
    # constraints = [
    #     models.UniqueConstraint(
    #         fields=['course_title', 'university'],
    #         name='unique_course_title_university'
    #     )
    # ]

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['email'])
        ]

    def __str__(self): # pylint: disable=invalid-str-returned
        return self.email
