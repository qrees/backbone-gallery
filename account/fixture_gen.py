from fixture_generator import fixture_generator

from django.contrib.auth.models import User
from account.models import Profile

@fixture_generator(User, Profile, export=True)
def test_users():
    user = Profile.objects.create(password='pass', username="simon", email="simon@example.com")
