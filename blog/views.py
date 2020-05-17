from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm, PostUser, PostAuth
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView, LogoutView


# Create your views here.  

class PostList(ListView):
    model = Post
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

def post_registration(request):

    if request.method == 'POST':
        f = PostUser(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('post_registration')
 
    else:
        f = PostUser()

    return render(request, 'blog/registration/post_registration.html', {
        'form': f
    })

