from django.urls import path
from . import views
from django.contrib.auth import views as dcviews

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/registration/', views.post_registration, name='post_registration'),
    path('post/login/', views.post_login, name='post_login'),
    path('post/logout/', views.post_logout, name='post_logout')
]