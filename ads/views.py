from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View, TemplateView, DeleteView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Ads, News, Answer, Author


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
        return context


class AnswerList(TemplateView):
    template_name = 'answer-list.html'

    def get_context_data(self, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        context = super().get_context_data(**kwargs)
        context['answers'] = Answer.objects.filter(ads__author=user.id).order_by('-date')
        return context

    def post(self, request, *args, **kwargs):
        # answer_id = request.POST['submit']
        print(request.POST)
        return super().get(request, *args, **kwargs)


class AnswerDelete(DeleteView):
    queryset = Answer.objects.all()
    template_name = 'answer-delete.html'
    context_object_name = 'answer'
    success_url = reverse_lazy('answers')


class AnswerDetail(DetailView):
    meta = Answer
    template_name = 'answer-detail.html'
    context_object_name = 'answer'
    queryset = Answer.objects.all()


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






