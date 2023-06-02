from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from ads.models import Ads, News, Answer, Author, Category
from ads.filters import AdsFilter, AnswerFilter


def index(request):
    '''Главная страница'''
    data = {
        'ads': Ads.objects.all(),
        'filter': AdsFilter(request.GET, queryset=Ads.objects.all())
    }
    return render(request, "index.html", context=data)


class AdsList(ListView):
    '''Список объявлений'''
    model = Ads
    template_name = 'ads-list.html'
    context_object_name = 'ads_list'
    paginate_by = 5 
    ordering = ['date']

    def get_filter(self):
        ads_filter = AdsFilter(self.request.GET, queryset=super().get_queryset())
        return ads_filter

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.get_filter()
        return context


class AdsDetail(DetailView):
    '''
    Страница объявления, с возможностью отправить отклин 
    на него в виде POST запроса
    '''
    model = Ads
    template_name = 'ads-detail.html'
    context_object_name = 'ads_detail'
    queryset = Ads.objects.all()

    def post(self, request, *args, **kwargs):
        author = Author.objects.get(authorUser=request.user)
        answer = Answer(
            text=request.POST['name'],
            ads_id=self.kwargs['pk'],
            author_id=author.id
        )
        answer.save()
        return super().get(request, *args, **kwargs) 


class NewsList(ListView):
    '''Список новостей'''
    model = News
    template_name = 'news-list.html'
    context_object_name = 'news_list'
    queryset = News.objects.all()
    paginate_by = 5 
    ordering = ['-date']


class NewsDetail(DetailView):
    '''Страница новости'''
    model = News
    template_name = 'news-detail.html'
    context_object_name = 'news_detail'
    queryset = News.objects.all()


class UserList(ListView): 
    '''Список пользователей'''
    model = User
    template_name = 'users-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['authors'] = Author.objects.all()
        return context


class AnswerList(ListView):
    '''Список откликов на объявления'''
    model = Answer
    context_object_name = 'answers'
    template_name = 'answer-list.html'

    def get_filter(self):
        user = User.objects.get(id=self.request.user.id)
        queryset=Answer.objects.filter(ads__author=user.id).order_by('-date')   
        return AnswerFilter(self.request.GET, queryset)

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.get_filter()
        context['answer_list'] = Answer.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        '''Принимаем/откланяем отклик'''
        answer_id = request.POST['answer']
        answer = Answer.objects.get(id=answer_id)
        if answer.status:
            answer.status = False
        else:
            answer.status = True
        answer.save()
        return super().get(request, *args, **kwargs)


class AnswerDelete(DeleteView):
    '''Удалить отклик'''
    queryset = Answer.objects.all()
    template_name = 'answer-delete.html'
    context_object_name = 'answer'
    success_url = reverse_lazy('answers')


class AnswerDetail(DetailView):
    '''Посмотреть отклик'''
    meta = Answer
    template_name = 'answer-detail.html'
    context_object_name = 'answer'
    queryset = Answer.objects.all()

    def post(self, request, *args, **kwargs):
        # answer_id = request.POST['submit']
        answer_id = request.POST['answer']
        answer = Answer.objects.get(id=answer_id)
        if answer.status:
            answer.status = False
        else:
            answer.status = True
        answer.save()
        return super().get(request, *args, **kwargs)


def author_list(request):
    '''Список авторов'''
    authors = Author.objects.all()
    return render(
        request, 
        'author_list.html', 
        context={'authors': authors},
        )


def author_detail(request, pk):
    '''Страница автора'''
    author = get_object_or_404(Author, id=pk)
    ads = Ads.objects.filter(author=author)
    context = {
        'author': author,
        'ads': ads,
    }
    return render(
        request, 
        'author_detail.html', 
        context
        )


class CategoryList(ListView):
    '''Список категорий'''
    model = Category
    context_object_name = 'category_list'
    template_name = 'cat-list.html'


def category_detail(request, pk):
    '''Описание категории'''
    cat = Category.objects.get(pk=pk)
    sub = cat.subscribers.all()
    return render(
        request, 
        'cat_detail.html', 
        {'category': cat,
         'subscribers': sub},
        )
    
@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user)
        return HttpResponse(f'{user.username}, вы отписались от категории {category.name}')
    else:
        category.subscribers.add(user)
        return HttpResponse(f'{user.username}, вы подписались на категорию {category.name}')