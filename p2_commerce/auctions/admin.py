from django.contrib import admin
from .models import *

class CommentInline(admin.TabularInline):
    model = Comment

class BidInline(admin.TabularInline):
    model = Bid
    
class AuctionAdmin(admin.ModelAdmin):
    filter_horizontal = ("liked_user",)
    inlines = [CommentInline, BidInline,]
    list_display = (
        "id",
        "user",
        "title",
        "price",
        "description",
        "category",
        "condition",
        "is_open",
    )

class UserAdmin(admin.ModelAdmin):
    inlines = [CommentInline,]

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Bid)
