from .models import User, Post
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        exclude = ["user", "commenters"]


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["name", "username", "email", "password1", "password2"]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["avatar", "username", "name", "bio"]