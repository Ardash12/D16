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
    template_name = 'accounts.html'

    def get_context_data(self, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        author = Author.objects.get(authorUser=User.objects.get(id=self.request.user.id))   # создаем объект класса текущего пользователя
        ads = Ads.objects.filter(author=author)   # создаем список объявлений текущего пользователя
        # добавить проверку
        answers_to_my_ads = []
        for ad in ads:   # перебираем объявления пользователя
            ans = Answer.objects.filter(ads=ad)   # находит отклики на объявления
            if ans:   # проверяем на наличие отклика перед записью в список
                answers_to_my_ads.append(ans)   # из-за этого приходится делать двойную распаковку в шаблоне accoutts.html

        # answers_to_my_ads = Answer.objects.filter(ads=Ads.objects.filter(author=author))

        context = super().get_context_data(**kwargs)
        context['ads'] = Ads.objects.filter(author=author)
        context['author'] = author
        context['my_answers'] = Answer.objects.filter(author=author)
        context['answers_to_my_ads'] = answers_to_my_ads

        return context