from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Ads, News, Category, Author, Answer


class AdsAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Ads
        fields = '__all__'


class NewsAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class AdsAdmin(admin.ModelAdmin):
    form = AdsAdminForm


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm


admin.site.register(Ads, AdsAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Answer)
