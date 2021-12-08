from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.models import User
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
        text = request.POST['name']
        user = request.user
        user_id = request.user.id
        author = Author.objects.get(authorUser=user)
        # answer = Answer(text=f'{user},{user_id},{text}, {author}, {author.id}', ads_id=1, author_id=author.id)
        a1 = request.path
        a2 = request.method
        a3 = request.GET
        a4 = request.POST
        a5 = request.COOKIES
        a6 = request.session
        a7 = request.user
        # answer = Answer(text=f'{a1}, {a2}, {a3}, {a4}, {a5}, {a6}, {a7}', ads_id=1, author_id=author.id)
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


