
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("new-post", views.newpost_view, name='new-post'),
    path("following", views.following, name="following"),
    
    # API Routes
    path('posts/<int:post_id>/toggle_like', views.toggle_like_api, name='toggle_like'),
    path('posts/<int:post_id>/edit_post', views.edit_post_api, name='edit_post'),
    path('profile/<int:user_id>/toggle_follow', views.toggle_follow_api, name='toggle_follow')
]
