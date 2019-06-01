from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create(**params)


class PublicUserApiTests(TestCase):
    """
    Test the users public api
    """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
        Test creating the user with valid payload is successful
        """
        payload = {
            'email': 'test@app.com',
            'name': 'test_user',
            'password': 'secret',
        }

        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """
        Test creating a user already exists fails
        """
        payload = {
            'email': 'test@app.com',
            'password': 'secret',
        }

        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Test that the password has more than 5 characters
        """
        payload = {
            'email': 'test@app.com',
            'password': '1234',
        }

        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """
        Test that a token is created for the user
        """
        payload = {
            'email': 'test@app.com',
            'password': 'secret'
        }
        create_user(**payload)
        response = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """
        Test that the token is not created for invalid credentials
        """
        payload = {
            'email': 'test@app.com',
            'password': 'secret',
        }
        create_user(**payload)
        payload['password'] = '123456'

        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """
        Test that the token is not created if user doesn't exists
        """
        payload = {
            'email': 'test@app.com',
            'password': 'secret',
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missin_field(self):
        """
        Test that email and password fields are required
        """
        payload = {
            'email': 'test',
            'password': '',
        }
        response = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
