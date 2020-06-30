# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from posts.models import Comments


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Comments.objects.create(post=11,text='Hi there')