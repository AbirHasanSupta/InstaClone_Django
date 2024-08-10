from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm, MyUserCreationForm, PostForm
from .models import User, Post, Comment, Message
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import Paginator
from django.db.models import Q


def home(request):
    posts = Post.objects.all()
    comments = Comment.objects.all()
    users = User.objects.all()
    context = {"posts": posts, "comment": comments, 'users': users}
    return render(request, 'base/home.html', context)


def login_page(request):
    page = "login"
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "This email does not exist.")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "The password is incorrect.")
    context = {"page": page}

    return render(request, 'base/login.html', context)


def register_page(request):
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration.")
    return render(request, "base/login.html", context={"form": form})


def logout_user(request):
    logout(request)
    return redirect('home')


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    posts = user.post_set.all()
    context = {"user": user, "posts": posts}
    return render(request, 'base/profile.html', context)


def post_page(request, pk):
    post_page_tag = "post"
    post = Post.objects.get(id=pk)
    comments = post.comment_set.all()
    context = {"post": post, "comments": comments, "post_page_tag": post_page_tag}
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def create_post(request):
    form = PostForm()
    if request.method == "POST":
        Post.objects.create(
            user=request.user,
            description=request.POST.get('description'),
            image=request.FILES.get('image')
        )
        return redirect('profile', pk=request.user.id)
    return render(request, 'base/create_post.html', {'form': form})


@login_required(login_url='login')
def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.user != post.user:
        return HttpResponse('You are not allowed to do this.')
    if request.method == "POST":
        post.delete()
        return redirect('profile', pk=request.user.id)


@login_required(login_url='login')
def edit_post(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    if request.user != post.user:
        return HttpResponse('You are not allowed here.')
    if request.method == "POST":
        post.description = request.POST.get('description')
        post.image = request.FILES.get('image')
        post.save()
        return redirect('home')
    context = {"post": post, "form": form}
    return render(request, 'base/create_post.html', context)


@login_required(login_url='login')
def update_user(request, pk):
    user = User.objects.get(id=pk)
    form = UserForm(instance=user)
    if request.user != user:
        return HttpResponse('You are not allowed here.')
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/update-user.html', context)


@login_required(login_url='login')
def comment_user(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == "POST":
        Comment.objects.create(
            user=request.user,
            body=request.POST.get('body'),
            post=post
        )
        return redirect('post', pk=post.id)


@login_required(login_url='login')
def inbox(request):
    user = request.user
    user_messages = Message.get_message(user=user)
    active_direct = None
    directs = None
    if user_messages:
        message = user_messages[0]
        active_direct = message['user'].username
        directs = Message.objects.filter(user=user, recipient=message['user'])
        directs.update(is_read=True)

        for message in user_messages:
            if message['user'].username == active_direct:
                message['unread'] = 0
    context = {
            'directs': directs,
            'user_messages': user_messages,
            'active_direct': active_direct
    }

    return render(request, 'base/inbox.html', context=context)


@login_required(login_url='login')
def direct(request, username):
    user = request.user
    user_messages = Message.get_message(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, recipient__username=active_direct)
    directs.update(is_read=True)

    for message in user_messages:
        if message['user'].username == active_direct:
            message['unread'] = 0
    context = {
        'directs': directs,
        'user_messages': user_messages,
        'active_direct': active_direct
    }

    return render(request, 'base/inbox.html', context)


@login_required(login_url='login')
def send_message(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')

    if request.method == "POST":
        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user, body)
        return redirect('inbox')


def user_search(request):
    query = request.GET.get('q')
    context = {}
    if query:
        users = User.objects.filter(Q(username__icontains=query))

        paginator = Paginator(users, 8)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

        context = {
            'users': users_paginator,

        }
    return render(request, 'base/search.html', context)


@login_required(login_url='login')
def new_message(request, username):
    from_user = request.user
    body = 'Hi'
    try:
        to_user = User.objects.get(username=username)
    except Exception:
        return redirect('user_search')
    if from_user != to_user:
        Message.send_message(from_user, to_user, body)
        return redirect('inbox')




