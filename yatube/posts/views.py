from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import PostForm

from .models import Group
from .models import Post
from .models import User


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'posts': posts,
        'title': 'Главная страница Yatube',
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:10]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)


def profile(request, username):
    username = get_object_or_404(User, username=username)
    posts = username.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts_num = posts.count()
    title = 'Профайл пользователя ' + str(username.get_full_name())
    context = {
        'username': username,
        'title': title,
        'posts_num': posts_num,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    text = post.text
    text_title = text[:30]
    pub_date = post.pub_date
    author = post.author
    name = author.get_full_name()
    count_posts = author.posts.all().count()
    group = post.group
    context = {
        'text': text,
        'pub_date': pub_date,
        'name': name,
        'count_posts': count_posts,
        'author': author,
        'group': group,
        'text_title': text_title,

    }
    return render(request, template, context)


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
        form = PostForm(instance=post)
        return render(request, 'posts/post_create.html', {'form': form,
                                                          'is_edit': True})
    form = PostForm(request.POST, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(instance=post)
    return render(request, 'posts/post_create.html', {'form': form,
                                                      'is_edit': True})
