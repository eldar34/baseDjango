from django.urls import path
from . import views
from django.contrib.auth import views as dcviews

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/update/', views.UpdatePost.as_view(), name='post_update'),
    path('post/registration/', views.post_registration, name='post_registration'),
    path('post/login/', views.post_login, name='post_login'),
    path('post/logout/', views.post_logout, name='post_logout'),
    path('post/create/', views.CreatePost.as_view(), name='post_create'),
    path('post/<int:pk>/delete/', views.DeletePost.as_view(), name='post_delete')
]