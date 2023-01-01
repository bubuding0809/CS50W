from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from .forms import NewAuctionForm, NewCommentForm, NewBidForm

from .models import User, Auction, Image, Comment, Bid


def index(request):
    auctions = Auction.objects.filter(is_open=True)

    return render(request, "auctions/index.html", {
        "auctions": auctions,
    })

@login_required
def profile(request):
    user = request.user
    auctions = Auction.objects.filter(user=user).order_by('-date_created')
    
    return render(request, "auctions/profile.html", {
        "auctions": auctions 
    })
    
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        profile_image = request.FILES.get('profile_image')

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, profile_image=profile_image)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
    
@login_required
def create(request):
    context = {
        'form': NewAuctionForm()
    }
    
    if request.method == "POST":
        form = NewAuctionForm(request.POST or None, request.FILES or None)
        image_files = request.FILES.getlist('images')
        
        if form.is_valid():
            user = request.user
            title = form.data['title']
            price = form.data['price']
            description = form.data['description']
            details = form.data['details']
            category = form.data['category']
            condition = form.data['condition']
            
            auction = Auction.objects.create(
                user=user,
                title=title,
                price=price,
                description=description,
                details=details,
                category=category,
                condition=condition,
            )
                        
            for image_file in image_files:
                image_file = Image.objects.create(
                    auction=auction, 
                    image_file=image_file,
                )
            
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", context)
            
    return render(request, "auctions/create.html", context)


def listing(request, id):
    try:
        auction = Auction.objects.get(pk=id)
    except:
        message = "Listing not found"
        return render(request, "auctions/error.html", {
            "message": message
        })
    
    bids = Bid.objects.filter(auction=auction).order_by('-bid_amount')[:5]
    context = {
        "auction": auction,
        "comments": auction.comments.all().order_by('-date_created'),
        "bids": bids,
        "commentForm": NewCommentForm(),
        "bidForm": NewBidForm(),
    }
    return render(request, "auctions/listing.html", context)


def list_comments(request, id):
    comment_start = int(request.GET.get('start') or 0)
    comment_end = int(request.GET.get('end') or (comment_start + 4))
    
    auction = Auction.objects.get(pk=id)
    comments = auction.comments.all().order_by('-date_created')[comment_start:comment_end]

    data = []
    for comment in comments:
        obj = {}
        obj['user'] = comment.user.username
        obj['comment'] = comment.comment
        obj['time_diff'] = comment.get_time_diff()
        try:
            obj['profile_image'] = comment.user.profile_image.url
        except:
            obj['profile_image'] = None
        data.append(obj)
    
    return JsonResponse(data, safe=False)


@login_required
def comment(request, id):
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        
        if form.is_valid():
            user = request.user
            auction = Auction.objects.get(pk=id)
            comment = form.cleaned_data['comment']
            Comment.objects.create(user=user, auction=auction, comment=comment)
            bids = Bid.objects.filter(auction=auction).order_by('-bid_amount')[:5]
            return render(request, "auctions/listing.html", {
                "auction": auction,
                "comments": Comment.objects.filter(auction=auction).order_by('-date_created'),
                "bids": bids,
                "commentForm": NewCommentForm(),
                "bidForm": NewBidForm(),
                "onload": 'onload="moveWin()"'
            })
        else:
            return HttpResponseRedirect(reverse("listing", kwargs={'id': id}))
    return HttpResponseRedirect(reverse("listing", kwargs={'id': id}))
    

@login_required    
def bid(request, id):
    if request.method == "POST":
        form = NewBidForm(request.POST)
        
        if form.is_valid():
            user = request.user
            auction = Auction.objects.get(pk=id)
            bid_amount = form.cleaned_data['bid_amount']
            
            if bid_amount <= auction.price:
                message = "Your new bid must be higher than the current bid, please place a new one"
                return render(request, "auctions/error.html", {
                    "message": message
                })
            
            if auction.is_open:    
                Bid.objects.create(user=user, auction=auction, bid_amount=bid_amount)
                auction.price = bid_amount
                auction.save()
                
                #Adds auction to user's watchlist
                if auction not in user.watchlist.all():
                    auction.liked_user.add(user)
            
            return HttpResponseRedirect(reverse("listing", kwargs={'id': id}))
        else:
            return HttpResponseRedirect(reverse("listing", kwargs={'id': id}))  
    
    return HttpResponseRedirect(reverse("listing", kwargs={'id': id}))    
    
    
@login_required    
def watchlist(request):
    user = request.user
    auctions = user.watchlist.filter(is_open=True)
    
    return render(request, "auctions/watchlist.html", {
        "auctions": auctions,
    })
    
    
def categories(request):
    categories = Auction.CATEGORY_CHOICES
    category_list = [Auction.objects.filter(category=pair[0], is_open=True) for pair in categories]
    
    return render(request, "auctions/categories.html", {
        "categories": zip(categories, category_list)
    })
    
    
def filtered(request, category):
    auctions = Auction.objects.filter(category=category, is_open=True)
    
    return render(request, "auctions/filtered.html", {
        "auctions": auctions,
    }) 
    
    
@login_required
def add_to_watchlist(request, id, origin):
    if request.method == "POST":
        user = request.user
        auction = Auction.objects.get(pk=id)

        if auction in user.watchlist.all():
            auction.liked_user.remove(user)
        else:
            auction.liked_user.add(user)

        if origin == "listing":
            return HttpResponseRedirect(reverse(origin, kwargs={"id": id}))
        elif origin == "filtered":
            return HttpResponseRedirect(reverse(origin, kwargs={"category": auction.category}))

        return HttpResponseRedirect(reverse(origin))
    
    return HttpResponseRedirect(reverse("listing", kwargs={"id": id}))


@login_required
def change_status(request, id):
    if request.method == "POST":
        auction = Auction.objects.get(pk=id)
        if auction.is_open:
            auction.is_open = False
            auction.save()
        else:
            auction.is_open = True
            auction.save()
            
        return HttpResponseRedirect(reverse("listing", kwargs={"id": id}))
    
    return HttpResponseRedirect(reverse("listing", kwargs={"id": id}))


def search(request):
    query = request.GET['q']
    auctions = Auction.objects.filter(title__icontains=query, is_open=True)
    
    return render(request, "auctions/search.html", {
        'auctions': auctions
    })