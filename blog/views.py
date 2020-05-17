from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm, PostUser, PostAuth
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView


# Create your views here.  

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

def post_list(request):
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = Post.objects.order_by('published_date')
    return render(request, 'blog/post_list.html', {
        'posts': posts
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {
        'post': post
    })

def post_edit(request, pk):

    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

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

def post_login(request):
    
    if request.method == 'POST':
        
        form = PostAuth(request.POST)
        print(form.is_valid())
        print('hello')
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('post_list')
                    # return HttpResponse('Authenticated successfully')
                else:
                    # return HttpResponse('Disabled account')
                    messages.success(request, 'Disabled account')
                    return redirect('post_login')                    
            else:
                # return HttpResponse('Invalid login')
                messages.success(request, 'Invalid login')
                return redirect('post_login') 
    else:
        form = PostAuth()

    return render(request, 'blog/registration/post_login.html', {
        'form': form
    })

def post_logout(request):
    logout(request)
    return redirect('post_list')
