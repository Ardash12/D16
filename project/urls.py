"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from ads.views import index, NewsList, NewsDetail, UserList, AnswerList, author_list, author_detail, \
    AnswerDetail, AnswerDelete


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ads/', include('ads.urls')),
    path('', index),
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('users/', UserList.as_view(), name='users'),
    path('answers/', AnswerList.as_view(), name='answers'),
    path('answer/<int:pk>', AnswerDetail.as_view(), name='answer'),
    path('answer_delete/<int:pk>', AnswerDelete.as_view(), name='answer_delete'),
    path('temp/', author_list),
    path('temp/<int:pk>', author_detail, name='temp2'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
