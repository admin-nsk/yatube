from django.shortcuts import render, get_object_or_404
from .models import Group


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.order_by("-pub_date")[:12]
    return render(request, "group.html", {"group": group, "posts": posts})


