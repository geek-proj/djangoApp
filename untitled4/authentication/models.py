# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
# Create your models here.
from django.urls import reverse


class CustomUser(AbstractUser):
    phone = models.CharField(
        max_length=50,
        blank=True,
    )
    image = models.ImageField(
        upload_to='media/',
        max_length=100
    )
    activationKey = models.CharField(
        max_length=100
    )
    class Meta:
        verbose_name = "CustomUser"
        verbose_name_plural = "CustomUser"
    def __str__(self):
        return self.username
    def get_absolute_url(self):
        return reverse("registration")