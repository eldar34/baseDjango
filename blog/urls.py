from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from . import views, api

urlpatterns = format_suffix_patterns([
    path('', views.PostList.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', views.UpdatePost.as_view(), name='post_update'),
    path('post/registration/', views.RegistrationPost.as_view(), name='post_registration'),
    path('post/login/', views.LoginPost.as_view(), name='post_login'),
    path('post/logout/', views.LogoutPost.as_view(), name='post_logout'),
    path('post/create/', views.CreatePost.as_view(), name='post_create'),
    path('post/<int:pk>/delete/', views.DeletePost.as_view(), name='post_delete'),
    path('registration-api/activate/<str:uid>/<str:token>/', views.UserActivationView.as_view()),
    
    path('api/v1/post/', api.PostReadViewSet.as_view({'get': 'list'}), name='post_view_set'),
    path('api/v1/post/<int:pk>', api.PostReadViewSet.as_view({'get': 'retrieve'}), name='post_retrieve'),
    path('api/v1/post/update/<int:pk>', api.PostEditGeneric.as_view(), name='post_api_update'),
    path('api/v1/post/create/', api.PostCreateGeneric.as_view(), name='post_api_create'),
    path('api/v1/post/delete/<int:pk>', api.PostDeleteGeneric.as_view(), name='post_api_delete'),
    
])

