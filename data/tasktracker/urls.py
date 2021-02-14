from django.urls import path

from . import views

#app_name = "articles"


urlpatterns = [
    path('', views.index, name='index'),
    path('user/create/', views.UserCreateView.as_view(), name='user_create'),
    path('api/actions/', views.ActionView.as_view()),
    path('api/users/', views.UserView.as_view()),
]