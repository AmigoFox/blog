from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse


class LoginRedirectTests(TestCase):
	def test_successful_login_redirects_to_blog_index(self):
		get_user_model().objects.create_user(
			username='reader', password='test-password'
		)

		response = self.client.post(
			reverse('users:login'),
			{'username': 'reader', 'password': 'test-password'},
		)

		self.assertRedirects(response, reverse('blogs:index'))

	def test_legacy_profile_url_redirects_to_blog_index(self):
		response = self.client.get('/accounts/profile/')

		self.assertRedirects(response, reverse('blogs:index'))
