from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import BlogPost


class BlogPostTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username='author', password='pass12345!')
        cls.other = User.objects.create_user(username='other', password='pass12345!')
        cls.post = BlogPost.objects.create(title='First', text='text one', owner=cls.author)

    def test_index_order_newest_first(self):
        newer = BlogPost.objects.create(title='Newer', text='t', owner=self.author)
        response = self.client.get(reverse('blogs:index'))
        posts = list(response.context['posts'])
        self.assertEqual(posts[0], newer)
        self.assertEqual(posts[1], self.post)

    def test_index_empty_message(self):
        BlogPost.objects.all().delete()
        response = self.client.get(reverse('blogs:index'))
        self.assertContains(response, 'Записей пока нет')

    def test_index_readable_anonymous(self):
        response = self.client.get(reverse('blogs:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First')

    def test_new_post_requires_login(self):
        response = self.client.get(reverse('blogs:new_post'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login/', response.url)

    def test_new_post_assigns_owner(self):
        self.client.login(username='author', password='pass12345!')
        self.client.post(reverse('blogs:new_post'), {'title': 'Mine', 'text': 'body'})
        post = BlogPost.objects.get(title='Mine')
        self.assertEqual(post.owner, self.author)

    def test_author_can_edit(self):
        self.client.login(username='author', password='pass12345!')
        response = self.client.post(
            reverse('blogs:edit_post', args=[self.post.id]),
            {'title': 'Changed', 'text': 'new body'},
        )
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Changed')

    def test_other_user_cannot_edit(self):
        self.client.login(username='other', password='pass12345!')
        response = self.client.get(reverse('blogs:edit_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 404)

    def test_missing_id_404(self):
        self.client.login(username='author', password='pass12345!')
        response = self.client.get(reverse('blogs:edit_post', args=[99999]))
        self.assertEqual(response.status_code, 404)

    def test_register_creates_and_logs_in(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'newbie',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newbie').exists())
        response = self.client.get(reverse('blogs:index'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout_get_does_not_logout(self):
        self.client.login(username='author', password='pass12345!')
        self.client.get(reverse('users:logout'))
        response = self.client.get(reverse('blogs:index'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout_post_logs_out(self):
        self.client.login(username='author', password='pass12345!')
        self.client.post(reverse('users:logout'))
        response = self.client.get(reverse('blogs:index'))
        self.assertFalse(response.context['user'].is_authenticated)
