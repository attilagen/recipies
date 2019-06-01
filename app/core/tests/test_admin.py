from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client


class AdminSiteTests(TestCase):

    def setUp(self):
        superuser = 'super@app.com'
        user = 'info@app.com'
        password = 'secret'

        self.client = Client()
        self.superuser = get_user_model().objects.create_superuser(
            email=superuser,
            password=password
        )
        self.client.force_login(self.superuser)

        self.user = get_user_model().objects.create_user(
            email=user,
            password=password
        )

    def test_users_listed(self):
        """
        Test that the user are listed on users page
        """

        url = reverse('admin:core_user_changelist')
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        """
        Test that the user edit page works
        """
        url = reverse('admin:core_user_change', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """
        Test that the user create page works
        """
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
