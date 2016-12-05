#question/urls.py
from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.question_list, name="question_list"),
    url(r'^detail/(?P<pk>[0-9]+)', views.detail_view, name="question_detail"),

]
