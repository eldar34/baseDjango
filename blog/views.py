from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, FormView
from django.views import View

from .models import Post
from .forms import PostRegistration
from .utils import AuthorPermissionMixin


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

class UpdatePost(AuthorPermissionMixin, UpdateView):

    login_url = 'post_login'

    model = Post
    fields = ['title', 'text']
    template_name = "blog/forms/post_edit_form.html"
    # template_name_suffix = '_edit_form'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.published_date = timezone.now()
        return super().form_valid(form)

class DeletePost(AuthorPermissionMixin, DeleteView):

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

class UserActivationView(View):
    def get(self, request, uid, token):  
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/auth/users/activation/"
        post_data = {'uid': uid, 'token': token, "url": "/auth/users/activation/"}
        # result = request.post(post_url, data = post_data)
        # content = result.text()
        return render(request, 'blog/api_auth.html', post_data)
        # return Response(post_data)
