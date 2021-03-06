from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.cache import cache_page

from .models import Post, User, Comments, Follow
from .form import PostForm, CommentForm

@cache_page(20, key_prefix='index_page')
def index(request):
    post_list = Post.objects.order_by('-pub_date').select_related('author').all()
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
        return render(request, 'new.html', {'form': form, 'post': None})
    form = PostForm()
    return render(request, 'new.html', {'form': form, 'post': None})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.select_related('author').filter(author=author)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    following = Follow.objects.filter(user=request.user.id, author=author.id).exists()
    return render(
        request,
        'profile.html',
        {
            'author': author,
            'page': page,
            'count': paginator.count,
            'following': following
        })


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.select_related('author').filter(author=author).count()
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.select_related('author').all()
    form = CommentForm()
    return render(request, 'post.html', {'author': author, 'post': post, 'count': posts, 'items': comments, 'form': form})


@login_required
def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=author)
    if request.user != author:
        return redirect("post", username=username, post_id=post_id)

    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect("post", username=request.user.username, post_id=post_id)
    return render(request, 'new.html', {'form': form, 'post': post})


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


def add_comment(request, username, post_id):
    # author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.select_related('author').filter(post=post_id)

    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post", username=username, post_id=post_id)
    return render(request, 'comments.html', {'form': form, 'items': comments, 'post': post})


@login_required
def follow_index(request):
    user_follows = User.objects.get(pk=request.user.id).follower.all().values_list('author')
    posts = Post.objects.select_related('author').filter(author__in=user_follows)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {'page': page, 'paginator': paginator})


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    subscribe = Follow.objects.create(user=request.user, author=author)
    subscribe.save()
    return redirect("follow_index")



@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    subscribe = Follow.objects.get(user=request.user.id, author=author.id)
    subscribe.delete()
    return redirect("follow_index")
