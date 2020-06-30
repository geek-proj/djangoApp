# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.utils.crypto import random
from .models import CustomUser
from django.http import HttpResponse
from django.views.generic.edit import FormView, CreateView
from django.views.generic.base import View, RedirectView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from .forms import CustomForm,CustomLoginForm
# Create your views here.

class RegistrationView(CreateView):
    model = CustomUser
    form_class = CustomForm
    template_name = 'registration.html'
    def post(self, request, *args, **kwargs):
        form = self.form_class(data=self.request.POST)
        randomKey = hashlib.sha1(str(random.random())).hexdigest()[:5]
        if form.is_valid():
            datas = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone'],
                'activationKey': hashlib.sha1(randomKey + form.cleaned_data['username']).hexdigest(),
                'password': form.cleaned_data['password'],
                'password2': form.cleaned_data['password2']
            }
            form.send_email(datas)
            form.save(datas)
            self.request.session['registered'] = True
            messages.success(self.request, 'Verification account is sent please verify your account')
            return redirect('/auth/registration')
        return render(request,'registration.html',{'form':form})
class LoginView(FormView):
    form_class = CustomLoginForm
    template_name = 'login.html'
    def form_valid(self, form):
        user = authenticate(self.request,
                            username=form.cleaned_data['username'],
                            password=form.cleaned_data['password']
                            )
        if user is not None:
            login(self.request,user)
        else:
            messages.error(self.request,'login or password wrong.')
        return redirect('/auth/login')
def index(request,key):
    user = get_object_or_404(CustomUser, activationKey=key)
    if not user.is_active and request.session['registered']:
        authMethod(user,request)
        user.is_active = True
        user.save()
        request.session['registered'] = False
    else:
        return redirect('/auth/registration')
    return HttpResponse("<h1>Thanks</h1>")
def authMethod( user,request):
    authed = authenticate(request, username=user.username, password=user.password)
    if authed is not None:
        login(request, authed)
    else:
        messages.error(request, 'password or username invalid')
class LogoutView(RedirectView):
    url = '/auth/registration/'
    def get(self, request, *args, **kwargs):
        print (request)
        django_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)