from django import test
from django.core.urlresolvers import reverse
from account.models import Profile


class AccountTest(test.TestCase):
    fixtures = ['test_users']

    def setUp(self):
        self.client = test.Client()

    def test_register_password_fail(self):
        url = reverse('account-register')
        result = self.client.post(url,
            data={
                'username': 'test',
                'email': 'test@example.com',
                'password1': 'pass',
                'password2': 'pass1'
            }
        )
        self.assertEqual(result.status_code, 200)
        self.assertQuerysetEqual(Profile.objects.filter(username='test'), [])

    def test_register_fail(self):
        url = reverse('account-register')
        result = self.client.post(url,
            data={
                'username': 'test',
                'email': 'simon@example.com',
                'password1': 'pass',
                'password2': 'pass'
            }
        )
        self.assertEqual(result.status_code, 200)
        self.assertQuerysetEqual(Profile.objects.filter(username='test'), [])

    def test_register(self):
        url = reverse('account-register')
        result = self.client.post(url,
            data={
                'username': 'test',
                'email': 'test@example.com',
                'password1': 'pass',
                'password2': 'pass'
            },
            follow=True
        )
        self.assertEqual(result.redirect_chain, [('http://testserver/account/login/', 302)])
        self.assertEqual(result.status_code, 200)
        self.assertQuerysetEqual(Profile.objects.filter(username='test'), ['<Profile: test>'])

    def test_login(self):
        url = reverse('account-login')
        result = self.client.post(url,
            data={
                'username': 'simon',
                'password': 'pass',
            },
            follow=True
        )
        self.assertEqual(result.redirect_chain, [('http://testserver/account/', 302)])
        self.assertEqual(result.status_code, 200)
