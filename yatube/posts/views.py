from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Post, User
from .form import PostForm


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, 'paginator': paginator})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('index')
        return render(request, 'new.html', {'form': form, 'new': True})
    form = PostForm()
    return render(request, 'new.html', {'form': form, 'new': True})


def profile(request, username):
    author = User.objects.get(username=username)
    posts = Post.objects.filter(author=author)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'author': author, 'page': page, 'count': paginator.count })


def post_view(request, username, post_id):
    author = User.objects.get(username=username)
    posts = Post.objects.filter(author=author).count()
    post = Post.objects.get(pk=post_id)
    return render(request, 'post.html', {'author': author, 'post': post, 'count': posts})


def post_edit(request, username, post_id):
    author = User.objects.get(username=username)
    post = Post.objects.get(pk=post_id)
    # тут тело функции. Не забудьте проверить,
    # что текущий пользователь — это автор записи.
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            if form.has_changed():
                form.instance.author = author
                form.save()
                return redirect('index')
        else:
            return render(request, 'new.html', {'form': form, 'new': False})
    else:
        if request.user.username == post.author.username:
            form = PostForm(instance=post)
            return render(request, 'new.html', {'form': form, 'new': False})
        else:
            return redirect(f'/{username}/{post_id}/')

