from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
import json

from .models import Post, User, PostMedia, PostLike, UserFollowing
from .forms import NewPostForm


# Authentication views************************************
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
# Network app views************************************
def index(request):
    posts = Post.objects.all()
    
    # Show 10 posts per page
    paginator = Paginator(posts, 10)
    
    # Retrieve page number requested from GET method
    page_number = request.GET.get('page')
    
    # Using paginator obj to get queryset of specified page number
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'postForm': NewPostForm()
    }
    
    return render(request, "network/index.html", context=context)


def profile(request, user_id):
    user = request.user
    try:
        if user_id:
            profile_user = User.objects.get(pk=user_id)
        elif not user.is_anonymous:
            profile_user = user
        else:
            raise PermissionDenied
    except:
        raise PermissionDenied
        
    posts = Post.objects.filter(user=profile_user)
    
    # Show 10 posts per page
    paginator = Paginator(posts, 10)
    
    # Retrieve page number requested from GET method
    page_number = request.GET.get('page')
    
    # Using paginator obj to get queryset of specified page number
    page_obj = paginator.get_page(page_number)
    
    followers = [obj.from_user for obj in profile_user.followers.all()]
    context = {
        'profile_user': profile_user,
        'followers': followers,
        'page_obj': page_obj
    }
    
    return render(request, 'network/profile.html', context=context)


@login_required
def following(request):
    user = request.user
    followings = [instance.to_user for instance in user.followings.all()]
    
    posts = Post.objects.filter(user__in = followings)
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj
    }
    
    return render(request, 'network/following.html', context=context)
    
        
@login_required
def newpost_view(request):
    if request.method == 'POST':
        user = request.user
        media_files = request.FILES.getlist('media')
    
        text_content = request.POST['text-content']
        
        post = Post.objects.create(
            user=user,
            text_content = text_content,
        )
        
        for media in media_files:
            PostMedia.objects.create(
                user=user,
                post=post,
                media=media,
            )
        return redirect(reverse('index'))

    
    return redirect(reverse('index'))
    
   

# API VIEWS 
@login_required
def toggle_like_api(request, post_id):
    if request.method != 'POST':
        raise PermissionDenied
    
    user = request.user
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse(
            {'error': 'Post not found'},
            status=404    
        )
    
    responseData = {}
    
    liked_user_list = [likeInstance.user for likeInstance in post.liked_users.all()]
    if user not in liked_user_list:
        PostLike.objects.create(
            user=user,
            post=post
        )
        
        responseData['message'] = f'Post {post_id} was liked by {user.username}'
    else:
        instance = PostLike.objects.get(
            user=user,
            post=post
        )
        instance.delete()
        
        responseData['message'] = f'Post {post_id} was unliked by {user.username}'
    
    responseData['like_count'] = post.liked_users.all().count()
        
    return JsonResponse(data=responseData, safe=False, status=200)

@login_required
def toggle_follow_api(request, user_id):
    if request.method != 'PUT':
        raise PermissionDenied
    
    user = request.user
    
    try:
        to_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse(
            {'error': 'User not found'},
            status=404
        )
    
    responseData = {}
    
    try:
        follow_pair = UserFollowing.objects.get(from_user=user, to_user=to_user) 
    except UserFollowing.DoesNotExist:
        UserFollowing.objects.create(from_user=user, to_user=to_user)
        responseData['message'] = f'User {to_user} was followed by {request.user}'
    else:
        follow_pair.delete()
        responseData['message'] = f'User {to_user} was unfollowed by {request.user}'
    
    responseData['follower_count'] = to_user.followers.all().count()
    
    return JsonResponse(data=responseData, safe=False, status=200)
    
@login_required
def edit_post_api(request, post_id):
    if request.method != 'PUT':
        raise PermissionDenied
    
    user = request.user
    try:
        post = Post.objects.get(user=user,id=post_id)
    except Post.DoesNotExist:
        return JsonResponse(
            {'error': 'Post not found'},
            status=404
        )
    
    responseData = {}
    
    # Get data sent via POST request
    data = json.loads(request.body)
    new_content = data.get('new_content')
    
    # Update post's text content with new content
    post.text_content = new_content
    post.save()
    
    responseData['message'] = f'post {post_id} has been updated with new content'
    responseData['new_content'] = new_content
    
    return JsonResponse(data=responseData, status=200)
    
    
    