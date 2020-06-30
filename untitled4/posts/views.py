# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import View, CreateView
from django.views.generic.detail import DetailView
from .models import *
from .forms import CommentForm,PostForm
# Create your views here.
class PostsView(View):
    http_method_names = ['get','post']
    form_class = PostForm
    template_name = 'home.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class
        countComments = {
            'posts':[]
        }
        count = 0
        for post in Posts.objects.all():
            count = count + 1
            comments = Comments.objects.all().filter(post=post).count()
            dict = {
                'post':post,
                'count':comments,
                'ids':count
            }
            countComments['posts'].append(dict)
        return render(request,self.template_name,{'form':form,'countComments':countComments})
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            user = request.user
            form.save(user)
            return redirect('/home')
        context = {
            'form':form,
        }
        return render(request,self.template_name,context)
class CommentDetailView(DetailView):
    model = Posts
    http_method_names = ['get', 'post']
    def get(self, request, *args, **kwargs):
        post_id = get_object_or_404(self.model,id=kwargs['id'])
        comments = Comments.objects.all().filter(post=post_id)
        data = serializers.serialize('json', comments)
        return HttpResponse(data, content_type="application/json")
class CommentCreateView(CreateView):
    model = Posts
    def post(self,request,*args,**kwargs):
        if request.POST and request.is_ajax:
            post = get_object_or_404(self.model, id=kwargs['id'])
            form = CommentForm(request.POST)
            if form.is_valid():
                form.save(post=post)
                serializer = serializers.serialize("json",Comments.objects.all().filter(post=post))
                return JsonResponse({'form':serializer},status=200)
        return JsonResponse({"error":"error"},status=400)