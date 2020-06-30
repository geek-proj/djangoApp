# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from authentication.models import *

# Create your models here.
class General(models.Model):
    date = models.DateTimeField(default=datetime.now())
    text = models.TextField(
        max_length=400
    )
    class Meta:
        abstract = True

class Posts(General):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=False
    )
    image = models.ImageField(
        upload_to='media/'
    )
    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('posts')

    class Meta:
        verbose_name = 'posts'
        verbose_name_plural = 'posts'
        ordering = ['date']

class Comments(General):
    post = models.ForeignKey(
        Posts,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('posts')

    class Meta:
        verbose_name = 'comments'
        verbose_name_plural = 'comments'
        ordering = ['date']
