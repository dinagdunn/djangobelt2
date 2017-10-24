# # -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class QuoteManager(models.Manager):
    def quote_validator(self, postData): 
        q_errors = {}
        if len(postData['quoted']) < 3:
            q_errors['quoted'] = "Quoted by must be more than 3 characters"
        if len(postData['msg']) < 10:
            q_errors['message'] = "Message must be more than 10 characters"
        return q_errors

class UserManager(models.Manager):
    def validator(self, postData): 
        errors ={}
        if len(postData['name']) < 3:
            errors['name_error'] = "Name must be 3 characters or more"
        if len(postData['alias']) < 3:
            errors['alias_error'] = "Alias must be 3 characters or more"
        if len(postData['password']) < 8:
            errors['pass_len'] = "*Passwords must be 8 characters or more"
        if not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = "Please enter a valid email address" 
        if postData['password'] != postData['confirm_password']:
            errors['pass_match'] = "Passwords do not match"
        if User.objects.filter(alias=postData['alias']):
            errors['exists'] = "Alias has already been taken"
        return errors
       
    def login(self, postData):
        user_check = User.objects.filter(email=postData['email'])
        if len(user_check) > 0:
            user_check = user_check[0] 
            if bcrypt.checkpw(postData['password'].encode(), user_check.password.encode()):
                user = {'user': user_check} 
                return user
            else:
                errors = {'errors': "Invalid Login. Please try again"}
                return errors
        else:
            errors = {'errors': "Invalid Login. Please try again"}
            return errors



class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length = 255)
    bday = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects=UserManager()

class Quote(models.Model):
    user = models.ForeignKey(User, related_name="posted_by")
    quoted_by = models.CharField(max_length = 255)
    message = models.TextField()
    users = models.ManyToManyField(User, related_name="quotes")
    created_at = models.DateTimeField(auto_now_add = True) 
    objects=QuoteManager()

