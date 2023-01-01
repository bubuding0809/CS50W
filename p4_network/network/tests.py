from django.test import TestCase
from django.db import IntegrityError
from .models import User, UserFollowing

# Create your tests here.
class FollowTests(TestCase):
    def test_no_self_follow(self):
        user = User.objects.create()
        constraint_name = 'network_UserFollowing_prevent_self_follow'
        with self.assertRaisesMessage(IntegrityError, constraint_name):
            UserFollowing.objects.create(user=user, user_following=user)
        