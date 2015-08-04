from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='url_shrtnr/index.html')),
    url(r'^api/$', views.UrlAPI.as_view()),
]
