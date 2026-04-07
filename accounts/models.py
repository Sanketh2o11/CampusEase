from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        # Superusers default to 'cr' role if no role is explicitly provided, 
        # but realistically they are admins. We'll set them as 'cr' just in case.
        extra_fields.setdefault('role', 'cr')

        return self.create_user(email, password, **extra_fields)


class Batch(models.Model):
    name = models.CharField(max_length=100, help_text="e.g., Class of 2026")
    year = models.IntegerField(help_text="e.g., 2026")
    department = models.CharField(max_length=100, help_text="e.g., Computer Science")

    def __str__(self):
        return f"{self.name} - {self.department}"

    class Meta:
        verbose_name_plural = "Batches"


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('cr', 'Class Representative'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def is_cr(self):
        return self.role == 'cr'
    
    @property
    def is_student(self):
        return self.role == 'student'
