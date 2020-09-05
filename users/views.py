from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import CustomUserCreationForm
from .models import CustomUser
from blog.models import Post
from django.urls import reverse_lazy

# Create your views here.

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'user/signup.html'

class UpdateUserView(UpdateView):
    model = CustomUser
    template_name = 'update.html'
    fields = ('first_name', 'last_name',
              'email', 'image', 'cv',
              'facebook', 'twitter', 'instagram',
              'linkdin',
    )

def author_info(request, author):
    author = get_object_or_404(CustomUser, username=author)
    success_url = reverse_lazy('login')
    author_posts = Post.objects.filter(author=author)
    return render(request, 'blog/author.html', {'author':author, 'author_posts':author_posts})