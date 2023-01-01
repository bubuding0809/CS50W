from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("create", views.create, name = "create"),
    path("search", views.search, name="search"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.filtered, name="filtered"),
    path("list_comments/<int:id>", views.list_comments, name="list_comments"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("listing/<int:id>/comment", views.comment, name="comment"),
    path("listing/<int:id>/bid", views.bid, name="bid"),
    path("listing/<int:id>/add_to_watchlist/<str:origin>", views.add_to_watchlist, name="add_to_watchlist"),
    path("listing/<int:id>/change_status", views.change_status, name="change_status"),
]
