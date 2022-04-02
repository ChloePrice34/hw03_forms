from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from yatube.settings import posts_per_page
from .forms import PostForm
from .models import Group
from .models import Post
from .models import User


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()
    paginator = Paginator(posts, posts_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'posts': posts,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, posts_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)


def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=user_profile)
    posts_count = user_posts.count()
    paginator = Paginator(user_posts, posts_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': user_profile,
        'page_obj': page_obj,
        'count': posts_count,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    user_post = get_object_or_404(Post, pk=post_id)
    posts = Post.objects.filter(author_id=user_post.author_id)
    posts_count = posts.count()
    context = {
        'post': user_post,
        'posts_count': posts_count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    template = 'posts/post_create.html'
    select_group = Group.objects.all()
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('posts:profile', username=request.user.username)
    context = {
        'form': form,
        'select_group': select_group,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    if request.method != 'POST':
        form = PostForm(request.POST or None, instance=post)
        return render(request, 'posts/post_create.html', {'form': form,
                                                          'is_edit': True})
    form = PostForm(request.POST, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
