from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.models import User
from .models import Ads, News, Answer


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
        user = request.user.username
        user_id = request.user_authorUser.id
        answer = Answer(text=user, status=True, ads_id=1, author_id=user_id)
        answer.save()
        # product = Product(name=name, quantity=quantity, category_id=category_id,
        #                   price=price)  # создаём новый товар и сохраняем
        # product.save()
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


class UserList(ListView):
    model = User
    template_name = 'users-list.html'
    context_object_name = 'users'
    queryset = User.objects.all()
