from django_filters import FilterSet
from django import forms
from django.db import models
from .models import Ads, Answer


class AnswerFilter(FilterSet):
    class Meta:
        model = Answer
        fields = ['author', 'ads',]


class AdsFilter(FilterSet):
    class Meta:
        model = Ads
        fields = ('author', 'title', 'category', 'date',)
