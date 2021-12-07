from django.contrib import admin
from .models import Ads, News, Category, Author, Answer


admin.site.register(Ads)
admin.site.register(News)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Answer)

