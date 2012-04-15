from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from account.models import Profile

class ProfileBackend(object):
    def authenticate(self, username=None, password=None):
        user = Profile.objects.get(username=username).user
        if check_password(password, user.password):
            return user
        return None

    def get_user(self, user_id):
        return User.objects.get(pk=user_id)
