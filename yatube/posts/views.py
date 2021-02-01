from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Post
from .form import PostForm


def index(request):
    latest = Post.objects.order_by('-pub_date')[:10]
    output = []
    for item in latest:
        output.append(item.text)
    return render(request, 'index.html', {"posts": latest})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('index')
        return render(request, 'new.html', {'form': form})
    form = PostForm()
    return render(request, 'new.html', {'form': form})


