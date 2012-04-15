from django import test
from django.core.urlresolvers import reverse
from account.models import Profile


class AccountTest(test.TestCase):

    def setUp(self):
        self.client = test.Client()

    def test_register(self):
        url = reverse('account-register')
        result = self.client.post(url,
            data={
                'username': 'test',
                'password1': 'pass',
                'password2': 'pass'
            }
        )
        self.assertEqual(result.status_code, 200)
        self.assertQuerysetEqual(Profile.objects.filter(username='test'), [])

