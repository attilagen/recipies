from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """
        Test creating a new user with an email is successful
        """

        email = 'test@app.com'
        password = 'secret'

        user = get_user_model().objects.create_user(email=email,
                                                    password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test the email for the new user is normalized
        """

        email = 'test@APP.COM'
        password = 'secret'

        user = get_user_model().objects.create_user(email=email,
                                                    password=password)

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """
        Test creating new user with no email raises error
        """

        email = None
        password = 'secret'

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=email,
                                                 password=password)

    def test_create_new_superuser(self):
        """
        Test creating a new superuser
        """

        email = 'test@APP.COM'
        password = 'secret'

        user = get_user_model().objects.create_superuser(email=email,
                                                         password=password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
