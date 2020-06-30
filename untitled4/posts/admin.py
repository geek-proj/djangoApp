# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Posts,Comments
# Register your models here.
admin.site.register(Posts)
admin.site.register(Comments)