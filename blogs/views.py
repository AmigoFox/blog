from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BlogPostForm
from .models import BlogPost


def index(request):
    posts = BlogPost.objects.order_by('-date_added')
    return render(request, 'blogs/index.html', {'posts': posts})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect('blogs:index')
    else:
        form = BlogPostForm()
    return render(request, 'blogs/new_post.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, owner=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blogs:index')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blogs/edit_post.html', {'form': form, 'post': post})