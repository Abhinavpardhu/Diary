from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from authentication.models import Profile

class AuthenticationTests(TestCase):
    def setUp(self):
        # Create a test user
        self.username = 'testuser'
        self.password = 'securepassword123'
        self.email = 'testuser@example.com'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email,
            first_name='Test',
            last_name='User'
        )

    def test_register_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_post_valid(self):
        register_url = reverse('register')
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newsecurepass123',
            'password2': 'newsecurepass123',
        }
        response = self.client.post(register_url, form_data)
        # Should redirect to home
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        # User should be created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        # Profile should be created automatically by signals
        new_user = User.objects.get(username='newuser')
        self.assertTrue(hasattr(new_user, 'profile'))

    def test_login_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_post_valid(self):
        login_url = reverse('login')
        form_data = {
            'username': self.username,
            'password': self.password,
        }
        response = self.client.post(login_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_login_post_invalid(self):
        login_url = reverse('login')
        form_data = {
            'username': self.username,
            'password': 'wrongpassword',
        }
        response = self.client.post(login_url, form_data)
        # Should render login page again with error
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logout(self):
        # Log in first
        self.client.login(username=self.username, password=self.password)
        logout_url = reverse('logout')
        response = self.client.get(logout_url)
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_profile_unauthenticated_redirect(self):
        profile_url = reverse('profile')
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 302)
        # Should redirect to login with next parameter
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_profile_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        profile_url = reverse('profile')
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_edit_profile_post_valid(self):
        self.client.login(username=self.username, password=self.password)
        edit_profile_url = reverse('edit_profile')
        
        # Mock image
        image_content = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
        mock_avatar = SimpleUploadedFile("avatar.gif", image_content, content_type="image/gif")
        
        form_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'bio': 'My new bio!',
            'avatar': mock_avatar,
        }
        response = self.client.post(edit_profile_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
        
        # Verify changes saved
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.user.profile.bio, 'My new bio!')
        self.assertTrue(self.user.profile.avatar.name.startswith('avatars/avatar'))

    def test_change_password_post_valid(self):
        self.client.login(username=self.username, password=self.password)
        change_password_url = reverse('change_password')
        form_data = {
            'old_password': self.password,
            'new_password1': 'newsecurepassword123',
            'new_password2': 'newsecurepassword123',
        }
        response = self.client.post(change_password_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
