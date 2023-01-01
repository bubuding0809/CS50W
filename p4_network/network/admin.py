from django.contrib import admin
from .models import *

class PostInline(admin.TabularInline):
    model = Post
    
class UserAdmin(admin.ModelAdmin):
    inlines = [PostInline,]

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(PostMedia)
admin.site.register(UserFollowing)
admin.site.register(PostLike)


