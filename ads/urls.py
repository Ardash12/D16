from django.urls import path
from .views import AdsList, AdsDetail, AdsUserList


urlpatterns = [
    path('', AdsList.as_view(), name='ads_list'),
    path('<int:pk>', AdsDetail.as_view(), name='ads_detail'),
    path('ads_user/', AdsUserList.as_view(), name='ads_user_list'),
]
