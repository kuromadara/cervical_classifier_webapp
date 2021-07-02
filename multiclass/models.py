from __future__ import unicode_literals
from django.db import models

class UserManager(models.Manager):
    def login_validator(self, postData):
        errors = {}

        if not UserRegistrationForm.objects.filter(username = postData['u_name']):
            errors["email"] = "This account does not exist. Please register."
            
        # Validation Rules for Login Password
        if len(postData['pass']) < 1:
            errors["pass"] = "Password is required"
        else:
            if not UserRegistrationForm.objects.filter(password = postData['pass']):
                errors["pass"] = "Password is not correct"

        return errors


class UserRegistrationForm(models.Model):
    username = models.CharField(max_length = 32)
    email = models.CharField(max_length = 32)
    password = models.CharField(max_length = 32)
    objects = UserManager()

class Meta:
    model = UserRegistrationForm
    fields = ("username","email","password",)

    

