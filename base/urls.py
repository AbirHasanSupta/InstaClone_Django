from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path('profile/<str:pk>', views.user_profile, name="profile"),
    path('post/<str:pk>', views.post_page, name="post"),
    path('create-post/', views.create_post, name="create_post"),
    path('delete-post/<str:pk>', views.delete_post, name="delete_post"),
    path('edit-post/<str:pk>', views.edit_post, name="edit_post"),
    path('update-user/<str:pk>', views.update_user, name="update_user"),
    path('comment_user/<str:pk>', views.comment_user, name="comment_user"),
    path('inbox/', views.inbox, name="inbox"),
    path('directs/<str:username>', views.direct, name="directs"),
    path('send/', views.send_message, name="send_message"),
    path('search/', views.user_search, name="user_search"),
    path('new/<username>', views.new_message, name="new"),
]