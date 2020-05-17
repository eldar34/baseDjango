from django.urls import path
from . import views
from django.contrib.auth import views as dcviews

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', views.UpdatePost.as_view(), name='post_update'),
    path('post/registration/', views.RegistrationPost.as_view(), name='post_registration'),
    path('post/login/', views.LoginPost.as_view(), name='post_login'),
    path('post/logout/', views.LogoutPost.as_view(), name='post_logout'),
    path('post/create/', views.CreatePost.as_view(), name='post_create'),
    path('post/<int:pk>/delete/', views.DeletePost.as_view(), name='post_delete')
]