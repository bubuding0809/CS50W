from datetime import datetime
from django.utils.timezone import utc
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_img = models.ImageField(upload_to='images/profile_images/', default='images/assets/default_image.png', verbose_name='')
    
    def __str__(self) -> str:
        return f'{self.username}'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text_content = models.TextField(max_length=500)
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timesatmp_last_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-timestamp_created']
        
    def __str__(self) -> str:
        return f"post {self.id}"
    
    def get_time_diff(self) -> str:
            now = datetime.utcnow().replace(tzinfo=utc)
            time_diff = (now - self.timestamp_created).total_seconds()
            
            if 0<time_diff<=60**2:
                if int(time_diff / 60) == 1:
                    return f"{int(time_diff / 60)} min ago"
                return f"{int(time_diff / 60)} mins ago"
            elif 60**2<time_diff<=(60**2)*24:
                if int(time_diff / 60**2) == 1:
                    return f"{int(time_diff / 60**2)} hour ago"
                return f"{int(time_diff / 60**2)} hours ago"
            else:
                if int(time_diff / 60**2*24) == 1:
                    return f"{int(time_diff / ((60**2)*24))} day ago"
                return f"{int(time_diff / ((60**2)*24))} days ago"
            
    def serialize(self):
        serialized_data = {
            'post_id': self.id,
            'user_name': self.user.username,
            'user_id': self.user.id,
            'user_image': self.user.user_img.url,
            'content': self.text_content,
            'timestamp': self.get_time_diff(),
            'liked_count': self.liked_users.count(),
            'liked_users': [liked_user.user.username for liked_user in self.liked_users.all()],
            'media': [media.media.url for media in self.media.all()],
        }
        
        return serialized_data
        

class UserFollowing(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings', null=True)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', null=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_followers",
                fields=['from_user','to_user'],  
            ),
            models.CheckConstraint(
                name='prevent_self_follow',
                check=~models.Q(from_user=models.F('to_user')),
            ),
        ]
        ordering = ["-timestamp"]
    
    def __str__(self) -> str:
        return f'{self.from_user} follows {self.to_user}'
    
    
class PostMedia(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='media')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    media = models.ImageField(upload_to='images/post_media/', verbose_name='')

    def __str__(self) -> str:
        return f'{self.media}'


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_users')
    timestamp = models.DateField(auto_now_add=True, db_index=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                name = 'unqiue_likes',
                fields= ['user', 'post'],
            )
        ]
        ordering = ["-timestamp"]
        
    def __str__(self) -> str:
        return f'{self.user} liked {self.post}'
    