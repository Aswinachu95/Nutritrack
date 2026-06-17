from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Food, MealLog, UserProfile

User = get_user_model()


class CoreAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'Password123!'
        }

        self.user = User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='Password123!'
        )
        self.profile = UserProfile.objects.get(user=self.user)

        self.food_idli = Food.objects.create(
            name='Idli',
            category='Breakfast',
            region='South India',
            is_vegetarian=True,
            calories=58,
            protein=2.0,
            carbs=12.0,
            fat=0.5,
            fiber=0.4,
        )

        self.food_dosa = Food.objects.create(
            name='Dosa',
            category='Breakfast',
            region='South India',
            is_vegetarian=True,
            calories=133,
            protein=3.5,
            carbs=18.0,
            fat=5.0,
            fiber=1.5,
        )

    def authenticate(self):
        response = self.client.post('/api/auth/token/', {
            'username': 'existing',
            'password': 'Password123!'
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_registration_creates_user_profile(self):
        response = self.client.post('/api/auth/register/', {
            'username': self.user_data['username'],
            'email': self.user_data['email'],
            'password': self.user_data['password'],
            'password2': self.user_data['password'],
        }, format='json')
        self.assertEqual(response.status_code, 201)

        user = User.objects.get(username=self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.user, user)

    def test_token_authentication(self):
        response = self.client.post('/api/auth/token/', {
            'username': 'existing',
            'password': 'Password123!'
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_profile_api_retrieve_and_update(self):
        self.authenticate()

        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('bmr', response.data)
        self.assertIn('target_calories', response.data)

        update_data = {
            'age': 35,
            'gender': 'female',
            'height_cm': 160,
            'weight_kg': 60.0,
            'activity_level': 'light',
            'goal': 'lose',
        }
        response = self.client.put('/api/profile/', update_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['age'], 35)
        self.assertEqual(response.data['gender'], 'female')
        self.assertGreater(response.data['bmr'], 0)
        self.assertGreater(response.data['target_calories'], 0)
        self.assertGreater(response.data['target_protein_g'], 0)
        self.assertGreater(response.data['target_carbs_g'], 0)
        self.assertGreater(response.data['target_fat_g'], 0)

    def test_daily_summary_returns_aggregated_macros(self):
        self.authenticate()
        MealLog.objects.create(
            user=self.user,
            food=self.food_idli,
            servings=2,
            meal_type='breakfast',
            eaten_at=date.today(),
        )
        MealLog.objects.create(
            user=self.user,
            food=self.food_dosa,
            servings=1,
            meal_type='breakfast',
            eaten_at=date.today(),
        )

        response = self.client.get(f'/api/daily-summary/?date={date.today()}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['calories'], 2 * 58 + 133)
        self.assertEqual(response.data['protein'], 2 * 2.0 + 3.5)
        self.assertEqual(response.data['carbs'], 2 * 12.0 + 18.0)
        self.assertEqual(response.data['fat'], 2 * 0.5 + 5.0)

    def test_food_list_search_and_filter(self):
        response = self.client.get('/api/foods/?search=Idli')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Idli')

        response = self.client.get('/api/foods/?category=Breakfast')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.data['count'], 2)
