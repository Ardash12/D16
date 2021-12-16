from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFromToRangeFilter
from .models import Ads, Answer

class AnswerFilter(FilterSet):
    ads = ModelChoiceFilter(queryset=Ads.objects.all())

    class Meta:
        model = Ads
        fields = ['ads']
