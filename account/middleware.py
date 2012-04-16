from account.models import Profile

class ProfileMiddleware(object):

    def process_request(self, request):
        request.actor = None
        if request.user.is_authenticated():
            try:
                request.actor = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                pass

