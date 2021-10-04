from django.db import models
import re
import bcrypt

# Create your models here.
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9.+_-]+@[a-zA_Z0-9._-]+\.[a-zA-z]+$')
NAME_REGEX = re.compile(r'[a-zA-Z]+$')

class UserManager(models.Manager):
    def reg_validator(self, post):
        errors = {}
        if len(post['first_name']) < 2:
            errors['first_name'] = "Your first name must be at least 2 characters"
        if len(post['last_name']) < 2:
            errors['last_name'] = "Your last name must be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post['email']):
            errors['email'] = "Invalid Email address"
        if len(User.objects.filter(email=post['email'])) > 0:
            errors['email'] = "Email already taken"
        if len(post['password']) < 8:
            errors['reg_pw'] = "Your password should be at least 8 characters"
        if post['password'] != post['confirm_password']:
            errors['confirm_pw'] = "Passwords do not match"
        return errors

    def log_validator(self, post):
        errors = {}
        if len(User.objects.filter(email=post['email'])) == 0:
            errors['login_em'] = "Invalid email"
        else:
            user = User.objects.get(email=post['email'])
            if not bcrypt.checkpw(post['password'].encode(), user.password.encode()):
                errors['login_pw'] = "Incorrect email/password combination"
        return errors

class JobManager(models.Manager):
    def job_validator(self, post):
        errors = {}
        if len(post['title']) < 3:
            errors['title'] = "Job title must be at least 3 characters"
        if len(post['location']) < 3:
            errors['location'] = "Job location must be at least 3 characters"
        if len(post['description']) < 3:
            errors['description'] = "Job description must be at least 3 characters"
        
        return errors

class CategoryManager(models.Manager):
    def cat_validator(self, post):
        errors = {}
        if len(post['categories']) < 1:
            errors['categories'] = ""
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Job(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    made_by_user = models.ForeignKey(User, related_name='jobs_made', on_delete=models.CASCADE)
    owned_by_user = models.ForeignKey(User, null=True, related_name='jobs_owned', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()

class Category(models.Model):
    name = models.CharField(max_length=255)
    jobs = models.ManyToManyField(Job, related_name="categories")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)