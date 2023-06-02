from django.urls import path
from ads import views


urlpatterns = [
    path('', views.index),
    path('ads/', views.AdsList.as_view(), name='ads_list'),
    path('ads/<int:pk>', views.AdsDetail.as_view(), name='ads'),
    path('news/', views.NewsList.as_view(), name='news_list'),
    path('news/<int:pk>', views.NewsDetail.as_view(), name='news'),
    path('users/', views.UserList.as_view(), name='users'),
    path('answer/', views.AnswerList.as_view(), name='answer_list'),
    path('answer/<int:pk>', views.AnswerDetail.as_view(), name='answer'),
    path('answer_delete/<int:pk>', views.AnswerDelete.as_view(), name='answer_delete'),
    path('author_list/', views.author_list),
    path('author/<int:pk>', views.author_detail, name='author'),
    path('category', views.CategoryList.as_view(), name='category_list'),
    path('category/<int:pk>', views.category_detail, name='category'),
    path('subscribe/<int:pk>', views.subscribe, name='subscribe'),
    
]
