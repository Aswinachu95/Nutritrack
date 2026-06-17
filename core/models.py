from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Food(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    is_vegetarian = models.BooleanField(default=True)
    calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()
    fiber = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class MealLog(models.Model):
    MEAL_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_logs')
    food = models.ForeignKey(Food, on_delete=models.PROTECT)
    servings = models.FloatField(default=1.0)
    meal_type = models.CharField(max_length=50, choices=MEAL_CHOICES)
    eaten_at = models.DateField()

    @property
    def calories_total(self):
        return self.food.calories * self.servings


class DietPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plans')
    name = models.CharField(max_length=200)
    target_calories = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user})"


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    ACTIVITY_CHOICES = [
        ('sedentary', 'Sedentary'),
        ('light', 'Lightly active'),
        ('moderate', 'Moderately active'),
        ('active', 'Active'),
        ('very_active', 'Very active'),
    ]
    GOAL_CHOICES = [
        ('lose', 'Lose weight'),
        ('maintain', 'Maintain weight'),
        ('gain', 'Gain weight'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Remove hard defaults so fields are intentionally blank until user provides values
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    height_cm = models.PositiveSmallIntegerField(null=True, blank=True)
    weight_kg = models.FloatField(null=True, blank=True)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, null=True, blank=True)
    goal = models.CharField(max_length=10, choices=GOAL_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    @property
    def bmr(self):
        # If any required value is missing, cannot compute BMR
        if self.gender is None or self.weight_kg is None or self.height_cm is None or self.age is None:
            return None
        if self.gender == 'male':
            value = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age + 5
        else:
            value = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age - 161
        return round(value, 1)

    @property
    def activity_multiplier(self):
        return {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9,
        }.get(self.activity_level, 1.55)

    @property
    def goal_multiplier(self):
        return {
            'lose': 0.85,
            'maintain': 1.0,
            'gain': 1.15,
        }.get(self.goal, 1.0)

    @property
    def target_calories(self):
        if self.bmr is None:
            return None
        return round(self.bmr * self.activity_multiplier * self.goal_multiplier)

    @property
    def target_protein_g(self):
        if self.target_calories is None:
            return None
        return round(self.target_calories * 0.25 / 4)

    @property
    def target_carbs_g(self):
        if self.target_calories is None:
            return None
        return round(self.target_calories * 0.45 / 4)

    @property
    def target_fat_g(self):
        if self.target_calories is None:
            return None
        return round(self.target_calories * 0.30 / 9)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
