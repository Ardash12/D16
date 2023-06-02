from datetime import datetime, timedelta
from django.utils.timezone import localtime
from django.contrib.auth.models import User
from celery import shared_task
from ads.models import Category, Ads


@shared_task
def mailing_ads():
    categories = Category.objects.all()
    week = datetime.date(localtime()) - timedelta(weeks=1)
    for category in categories:
        ads_list = Ads.objects.filter(category=category) & Ads.objects.filter(date__lt=week)
        mail_list = category.subscribers
        if ads_list:
            pass
            # print(ads_list.values('date'))
        elif mail_list:
            print('Mail', mail_list.values('username'))