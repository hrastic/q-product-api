"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Product(models.Model):
    """Product object."""
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    rating = models.FloatField()
    updated_at = models.DateField(null=True, auto_now=True)

    def __str__(self) -> str:
        return self.name


class Rating(models.Model):
    """Rating object."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_rating'
    )
    rating = models.IntegerField()

    def __str__(self) -> str:
        return str(self.user) + ' - ' + str(self.product)

    class Meta:
        unique_together = ('user', 'product')
