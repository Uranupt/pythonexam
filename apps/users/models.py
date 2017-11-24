# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
email_reg = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
import bcrypt
from datetime import datetime

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['name']) < 1:
            errors['nameleng'] = "Name is required."
        if len(postData['alias']) < 1:
            errors['nameleng'] = "Alias is required."
        if postData['alias'].isalpha() == False:
            errors['namealpha'] = "Alias must contain only letters."
        if not email_reg.match(postData['email']):
            errors['email'] = "Email is required and must be valid."
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['password'] != postData['pwcnfrm']:
            errors['pwcnfrm'] = "Password and confirmation must match."
        if not datetime.strptime(postData['dateob'], "%Y-%m-%d").date() < datetime.today().date():
            errors['dob'] = "Your date of birth must be before today!"
        return errors

    def logvalid(self, postData):
        errors = {}
        if not email_reg.match(postData['email']):
            errors['email'] = "Please enter a valid email."
        if len(postData['password']) < 8:
            errors['password'] = "Please enter a valid password."
        if len(self.filter(email=postData['email'])) == 0:
            errors['noaccount'] = "No user matching this email."
        elif not bcrypt.checkpw(postData['password'].encode(), (self.filter(email=postData['email'])[0].pw_hash).encode()):
                errors['incpw'] = "The password you entered was incorrect."
        return errors



class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    dob = models.DateField()
    pw_hash = models.CharField(max_length=255)
    objects = UserManager()

class Poke(models.Model):
    poker_id = models.ForeignKey(User, related_name="poker")
    poked_id = models.ForeignKey(User, related_name="poked")
    times = models.IntegerField()
# Create your models here.
