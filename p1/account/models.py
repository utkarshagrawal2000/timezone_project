from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.core.validators import RegexValidator


class UserManager(UserManager):
  def create_user(self, email,mobile, username, tc,is_admin, password=None, password2=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')
      if not mobile:
          raise ValueError('User must have an mobile')

      user = self.model(
          email=self.normalize_email(email),
          username=username,
          mobile=mobile,
          
          tc=tc,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, mobile,username, tc, password=None):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          password=password,
          username=username,
          mobile=mobile,
          is_admin=1,
          tc=tc,
      )
      user.is_admin = 1
      user.save(using=self._db)
      return user

mobile_validator = RegexValidator(r"^(\+?\d{0,4})?\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{4}\)?)?$", "The mobile number provided is invalid")


class User(AbstractUser):
    
    email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
    name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=200, validators=[mobile_validator], unique=True)
    tc = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.CharField(max_length=30,default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
 
    REQUIRED_FIELDS = ["mobile", "email","tc"]


    def __str__(self):
      return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        if self.is_admin:
            return 1

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
