from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import create_slug_shortcode
AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'apple': 'apple', 'email': 'email'}

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=False, is_staff=False, is_superuser=False, **kwargs):
        if not email:
            raise ValueError("Users must have an email adress")
        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email=self.normalize_email(email),
            is_active=True,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class MyUser(AbstractBaseUser):
    email = models.EmailField(
        unique=True, max_length=120, verbose_name='E-mail')
    username = models.CharField(max_length=100, blank=True, null=True, unique=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    slug = models.SlugField(unique=True)
    activation_token = models.CharField(max_length=255, blank=True, null=True)
    reset_code = models.CharField(max_length=254, blank=True, null=True)
    born_year = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    is_student = models.BooleanField(default=False)
    university_name = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    current_active_days = models.IntegerField(default=0)
    max_consecutive_active_days = models.IntegerField(default=0)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return True
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug_shortcode(size=12, model_=MyUser)
        return super(MyUser, self).save(*args, **kwargs)
    
    

