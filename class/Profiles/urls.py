#Profiles/urls.py
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^detail/(?P<user_id>[0-9]+)/', views.profile_detail, name="profile_detail_view"),
    url(r'^detail/edit$', views.profile_edit, name="edit_profile"),
    url(r'^list/(?P<list_type>[0-9])/', views.profile_list, name="profile_list_view"),

]
