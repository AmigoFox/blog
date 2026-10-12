from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import BlogPost


class HomePageTests(TestCase):
	def test_homepage_displays_blog_index(self):
		response = self.client.get('/')

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'blogs/index.html')


class DeletePostTests(TestCase):
	def setUp(self):
		self.owner = get_user_model().objects.create_user(
			username='owner', password='test-password'
		)
		self.post = BlogPost.objects.create(
			title='Test post', text='Post content', owner=self.owner
		)
		self.url = reverse('blogs:delete_post', args=[self.post.id])

	def test_owner_can_delete_post_with_post_request(self):
		self.client.force_login(self.owner)

		response = self.client.post(self.url)

		self.assertRedirects(response, reverse('blogs:index'))
		self.assertFalse(BlogPost.objects.filter(id=self.post.id).exists())

	def test_owner_cannot_delete_post_with_get_request(self):
		self.client.force_login(self.owner)

		response = self.client.get(self.url)

		self.assertEqual(response.status_code, 405)
		self.assertTrue(BlogPost.objects.filter(id=self.post.id).exists())

	def test_other_user_cannot_delete_post(self):
		other_user = get_user_model().objects.create_user(
			username='other', password='test-password'
		)
		self.client.force_login(other_user)

		response = self.client.post(self.url)

		self.assertEqual(response.status_code, 404)
		self.assertTrue(BlogPost.objects.filter(id=self.post.id).exists())
