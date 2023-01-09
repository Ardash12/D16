from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View, TemplateView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import BaseRegisterForm
from ads.models import Ads, News, Answer, Author


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    # success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        author = Author(authorUser=User.objects.get(id=user.id))
        author.save()
        return redirect('login')


class Account(LoginRequiredMixin, TemplateView):
    '''Личный кабинет'''
    template_name = 'accounts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = Author.objects.get(authorUser=User.objects.get(id=self.request.user.id))
        context['ads_count'] = Ads.objects.filter(author=author).count()
        context['my_answers_count'] = Answer.objects.filter(author=author).count()
        context['answers_to_my_ads_count'] = Answer.objects.filter(ads__author=author).count()
        return context
