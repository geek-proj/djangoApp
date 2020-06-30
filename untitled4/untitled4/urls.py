"""untitled4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from authentication.views import RegistrationView,LoginView,index,LogoutView
from posts.views import PostsView,CommentDetailView,CommentCreateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/registration/$',RegistrationView.as_view(),name='registration'),
    url(r'^auth/verify/(?P<key>.+)/$',index,name='index'),
    url(r'^logout/',LogoutView.as_view(),name='logout'),
    url(r'^auth/login/$',LoginView.as_view(),name='login'),
    url(r'^home/$',PostsView.as_view(),name='posts'),
    url(r'^home/post/(?P<id>.+)/$',CommentDetailView.as_view(),name='comment_detail'),
    url(r'^home/create/(?P<id>.+)/$',CommentCreateView.as_view(),name='comment_create'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)