from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostRegistration

from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm

# Create your views here.  

class PostList(ListView):
    model = Post
    paginate_by = 2
    queryset = Post.objects.order_by('published_date')

class PostDetail(DetailView):
    model = Post
    
class CreatePost(LoginRequiredMixin, CreateView):

    login_url = 'post_login'
    
    model = Post
    fields = ['title', 'text']    
    template_name = "blog/forms/post_edit_form.html"
    # template_name_suffix = '_edit_form'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()        
        return super().form_valid(form)

class UpdatePost(LoginRequiredMixin, UpdateView):

    login_url = 'post_login'

    model = Post
    fields = ['title', 'text']
    template_name = "blog/forms/post_edit_form.html"
    # template_name_suffix = '_edit_form'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin, DeleteView):

    login_url = 'post_login'

    model = Post
    template_name = "blog/forms/post_delete_form.html"
    # template_name_suffix = '_edit_form'
    success_url = reverse_lazy('post_list')

class LoginPost(LoginView):
    template_name = 'blog/registration/post_login.html'

class LogoutPost(LogoutView):
    template_name = 'blog/registration/post_login.html'

class RegistrationPost(FormView):

    template_name = 'blog/registration/post_registration.html'
    form_class = PostRegistration
    success_url = '/post/registration/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Account created successfully')
        return super().form_valid(form)
