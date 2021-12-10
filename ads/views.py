from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View, TemplateView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Ads, News, Answer, Author
from .forms import BaseRegisterForm


def index(request):
    data = {"header": "Hello Django", "message": "Welcome to Python"}
    return render(request, "index.html", context=data)


class AdsList(ListView):
    model = Ads
    template_name = 'ads-list.html'
    context_object_name = 'ads_list'
    queryset = Ads.objects.all()
    paginate_by = 5  # постраничный вывод
    ordering = ['date']


class AdsDetail(DetailView):
    model = Ads
    template_name = 'ads-detail.html'
    context_object_name = 'ads_detail'
    queryset = Ads.objects.all()

    def post(self, request, *args, **kwargs):
        # берём значения для нового товара из POST-запроса отправленного на сервер
        author = Author.objects.get(authorUser=request.user)
        answer = Answer(
            text=request.POST['name'],
            ads_id=self.kwargs['pk'],
            author_id=author.id
        )
        answer.save()
        return super().get(request, *args, **kwargs)  # отправляем пользователя обратно на GET-запрос.


class NewsList(ListView):
    model = News
    template_name = 'news-list.html'
    context_object_name = 'news_list'
    queryset = News.objects.all()
    paginate_by = 5  # постраничный вывод
    ordering = ['-date']   # сортируем, свежие сверху


class NewsDetail(DetailView):
    model = News
    template_name = 'news-detail.html'
    context_object_name = 'news_detail'
    queryset = News.objects.all()


class UserList(ListView):   # список пользователей
    model = User
    template_name = 'users-list.html'
    # context_object_name = 'users'
    # queryset = User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['authors'] = Author.objects.all()
        # context['temp'] = Author.objects.filter(authorUser__id=User)
        return context


class AnswerList(ListView):
    model = Answer
    template_name = 'answer-list.html'
    ordering = ['date']
    # context_object_name = 'answers'
    # queryset = Answer.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answers'] = Answer.objects.all()
        context['ads'] = Ads.objects.all()
        return context


def author_list(request):
    authors = Author.objects.all()
    return render(request, 'temp.html', context={'authors': authors})


def author_detail(request, pk):
    # author = Author.objects.get(id=pk)
    author = get_object_or_404(Author, id=pk)
    ads = Ads.objects.filter(author=author)
    context = {
        'author': author,
        'ads': ads,
    }
    return render(request, 'temp2.html', context)


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


class AnswerDetail(DetailView):
    meta = Answer
    template_name = 'answer-detail.html'
    context_object_name = 'answer'
    queryset = Answer.objects.all()


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    # success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        author = Author(authorUser=User.objects.get(id=user.id))
        author.save()
        return redirect('login')

