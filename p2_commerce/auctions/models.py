from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import utc
from datetime import datetime

class User(AbstractUser):
    profile_image = models.ImageField(upload_to='images/user_images/', null=True, blank=True, verbose_name="")
    
    
class Auction(models.Model):
    CATEGORY_CHOICES = [
        ('CR', 'Cars'),
        ('CT', 'Computers & Tech'),
        ('PT', 'Pets'),
        ('FD', 'Food & Drinks'),
        ('FS', 'Fashion'),
        ('TY', 'Toys'),
        ('HM', 'Home'),
    ]
    
    CONDITION_CHOICES = [
        ('BN', 'Brand new'),
        ('PT', 'Pristine'),
        ('SU', 'Slighty used'),
        ('OD', 'Old'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions", null=True)
    title = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=30)
    details = models.TextField(max_length=500, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True)
    is_open = models.BooleanField(default=True)
    liked_user = models.ManyToManyField(User, blank=True, related_name="watchlist")
    
    class Meta:
        ordering = ['-date_created']
    
    def __str__(self) -> str:
        return f"{self.title}"
    
    def get_time_diff(self):
        if self.date_created:
            now = datetime.utcnow().replace(tzinfo=utc)
            time_diff = (now - self.date_created).total_seconds()
            
            if 0<time_diff<=60**2:
                return f"{int(time_diff / 60)} mins ago"
            elif 60**2<time_diff<=(60**2)*24:
                if int(time_diff / 60**2) == 1:
                    return f"{int(time_diff / 60**2)} hour ago"
                else:
                    return f"{int(time_diff / 60**2)} hours ago"
            else:
                if int(time_diff / 60**2*24) == 1:
                    return f"{int(time_diff / ((60**2)*24))} day ago"
                else:
                    return f"{int(time_diff / ((60**2)*24))} days ago"

    def get_id_string(self):
        return f"auction{self.id}"
                
                
class Image(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="images", null=True)
    image_file = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="")
    
    def __str__(self) -> str:
        return f"Image saved at {str(self.image_file)}"
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=300)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self) -> str:
        return self.comment
    
    def get_time_diff(self) -> str:
        if self.date_created:
            now = datetime.utcnow().replace(tzinfo=utc)
            time_diff = (now - self.date_created).total_seconds()
            
            if 0<time_diff<=60**2:
                return f"{int(time_diff / 60)} mins ago"
            elif 60**2<time_diff<=(60**2)*24:
                if int(time_diff / 60**2) == 1:
                    return f"{int(time_diff / 60**2)} hour ago"
                else:
                    return f"{int(time_diff / 60**2)} hours ago"
            else:
                if int(time_diff / 60**2*24) == 1:
                    return f"{int(time_diff / ((60**2)*24))} day ago"
                else:
                    return f"{int(time_diff / ((60**2)*24))} days ago"
    
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    bid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self) -> str:
        return str(self.bid_amount)