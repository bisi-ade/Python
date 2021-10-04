from django.db import models
import bcrypt
import re

# Create your models here.
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9.+_-]+@[a-zA_Z0-9._-]+\.[a-zA-z]+$')
NAME_REGEX = re.compile(r'[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate(self, postData):
        errors = {}
        email = User.objects.filter(email=postData['email'])
        print('************',email)
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters"
        elif not NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = "First name must contain letters only"

        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters"
        elif not NAME_REGEX.match(postData['last_name']):
            errors['last_name'] = "Last name must contain letters only"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email format"
        elif len(User.objects.filter(email=postData['email'])) > 0:
            errors['email'] = "Email already registered"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"

        if postData['password'] != postData['pw_confirm']:
            errors['pw_confirm'] = "Password do not match"
        return errors

    def validate_login(self, postData):
        errors = {}
        if len(User.objects.filter(email = postData['email'])):
            user = User.objects.get(email = postData['email'])
            if bcrypt.checkpw(postData['password'].encode(), user.password):
                return errors
            else:
                errors['login'] = "Email/password incorrect"
                return errors
        else:
            errors['login'] = "Email/password incorrect"
            return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.BinaryField(max_length=255)
    confirm = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return "<User object: {} {} {}".format(self.first_name, self.last_name, self.email)

    objects = UserManager()