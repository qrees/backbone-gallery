from account.models import Profile

class ProfileMiddleware(object):

    def process_request(self, request):
        if request.user.is_authenticated():
            request.actor = Profile.objects.get(user=request.user)
        else:
            request.actor = None
