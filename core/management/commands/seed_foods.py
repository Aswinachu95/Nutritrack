from django.core.management.base import BaseCommand
from core.models import Food

FOOD_ITEMS = [
    {'name': 'Idli', 'category': 'Breakfast', 'region': 'South India', 'is_vegetarian': True, 'calories': 58, 'protein': 2.0, 'carbs': 12.0, 'fat': 0.5, 'fiber': 0.4},
    {'name': 'Dosa', 'category': 'Breakfast', 'region': 'South India', 'is_vegetarian': True, 'calories': 133, 'protein': 3.5, 'carbs': 18.0, 'fat': 5.0, 'fiber': 1.5},
    {'name': 'Chapati', 'category': 'Bread', 'region': 'North India', 'is_vegetarian': True, 'calories': 71, 'protein': 3.0, 'carbs': 15.0, 'fat': 1.0, 'fiber': 1.5},
    {'name': 'Dal Tadka', 'category': 'Main course', 'region': 'North India', 'is_vegetarian': True, 'calories': 150, 'protein': 8.0, 'carbs': 18.0, 'fat': 5.0, 'fiber': 4.0},
    {'name': 'Sambar', 'category': 'Soup', 'region': 'South India', 'is_vegetarian': True, 'calories': 90, 'protein': 4.0, 'carbs': 15.0, 'fat': 2.5, 'fiber': 3.0},
    {'name': 'Palak Paneer', 'category': 'Main course', 'region': 'North India', 'is_vegetarian': True, 'calories': 210, 'protein': 10.0, 'carbs': 8.0, 'fat': 15.0, 'fiber': 4.0},
    {'name': 'Chana Masala', 'category': 'Main course', 'region': 'North India', 'is_vegetarian': True, 'calories': 190, 'protein': 8.0, 'carbs': 28.0, 'fat': 5.5, 'fiber': 8.0},
    {'name': 'Paneer Bhurji', 'category': 'Main course', 'region': 'North India', 'is_vegetarian': True, 'calories': 220, 'protein': 11.0, 'carbs': 7.0, 'fat': 16.5, 'fiber': 2.0},
    {'name': 'Aloo Paratha', 'category': 'Bread', 'region': 'North India', 'is_vegetarian': True, 'calories': 260, 'protein': 5.0, 'carbs': 35.0, 'fat': 10.0, 'fiber': 3.5},
    {'name': 'Biryani', 'category': 'Main course', 'region': 'North India', 'is_vegetarian': False, 'calories': 290, 'protein': 12.0, 'carbs': 40.0, 'fat': 9.0, 'fiber': 3.0},
    {'name': 'Masala Chai', 'category': 'Beverage', 'region': 'All India', 'is_vegetarian': True, 'calories': 120, 'protein': 2.0, 'carbs': 18.0, 'fat': 4.5, 'fiber': 0.0},
    {'name': 'Raita', 'category': 'Side dish', 'region': 'North India', 'is_vegetarian': True, 'calories': 60, 'protein': 3.0, 'carbs': 5.0, 'fat': 3.0, 'fiber': 1.0},
    {'name': 'Gulab Jamun', 'category': 'Dessert', 'region': 'North India', 'is_vegetarian': True, 'calories': 150, 'protein': 2.0, 'carbs': 25.0, 'fat': 5.0, 'fiber': 0.5},
    {'name': 'Samosa', 'category': 'Snack', 'region': 'North India', 'is_vegetarian': True, 'calories': 260, 'protein': 4.0, 'carbs': 30.0, 'fat': 14.0, 'fiber': 2.0},
    {'name': 'Pongal', 'category': 'Breakfast', 'region': 'South India', 'is_vegetarian': True, 'calories': 215, 'protein': 6.0, 'carbs': 35.0, 'fat': 5.0, 'fiber': 2.0},
    {'name': 'Rasam', 'category': 'Soup', 'region': 'South India', 'is_vegetarian': True, 'calories': 40, 'protein': 2.0, 'carbs': 6.0, 'fat': 0.5, 'fiber': 1.0},
    {'name': 'Kadhi', 'category': 'Main course', 'region': 'North India', 'is_vegetarian': True, 'calories': 175, 'protein': 6.0, 'carbs': 18.0, 'fat': 9.0, 'fiber': 1.5},
    {'name': 'Vegetable Pulao', 'category': 'Main course', 'region': 'North India', 'is_vegetarian': True, 'calories': 205, 'protein': 5.0, 'carbs': 35.0, 'fat': 6.0, 'fiber': 4.0},
    {'name': 'Methi Thepla', 'category': 'Bread', 'region': 'West India', 'is_vegetarian': True, 'calories': 190, 'protein': 4.0, 'carbs': 25.0, 'fat': 7.0, 'fiber': 3.5},
    {'name': 'Rajma', 'category': 'Main course', 'region': 'North India', 'is_vegetarian': True, 'calories': 180, 'protein': 9.0, 'carbs': 30.0, 'fat': 3.5, 'fiber': 7.0},
    {'name': 'Paneer Tikka', 'category': 'Appetizer', 'region': 'North India', 'is_vegetarian': True, 'calories': 170, 'protein': 11.0, 'carbs': 8.0, 'fat': 11.0, 'fiber': 2.0},
    {'name': 'Butter Chicken', 'category': 'Main course', 'region': 'North India', 'is_vegetarian': False, 'calories': 320, 'protein': 15.0, 'carbs': 10.0, 'fat': 22.0, 'fiber': 1.5},
    {'name': 'Tandoori Chicken', 'category': 'Main course', 'region': 'North India', 'is_vegetarian': False, 'calories': 260, 'protein': 23.0, 'carbs': 5.0, 'fat': 16.0, 'fiber': 0.0},
    {'name': 'Aloo Gobi', 'category': 'Main course', 'region': 'North India', 'is_vegetarian': True, 'calories': 150, 'protein': 4.0, 'carbs': 18.0, 'fat': 7.0, 'fiber': 4.0},
    {'name': 'Dhokla', 'category': 'Snack', 'region': 'West India', 'is_vegetarian': True, 'calories': 160, 'protein': 5.0, 'carbs': 25.0, 'fat': 5.0, 'fiber': 1.5},
    {'name': 'Paneer Butter Masala', 'category': 'Main course', 'region': 'North India', 'is_vegetarian': True, 'calories': 300, 'protein': 13.0, 'carbs': 12.0, 'fat': 20.0, 'fiber': 2.5},
    {'name': 'Pav Bhaji', 'category': 'Street food', 'region': 'West India', 'is_vegetarian': True, 'calories': 240, 'protein': 6.0, 'carbs': 32.0, 'fat': 10.0, 'fiber': 4.0},
    {'name': 'Masala Dosa', 'category': 'Breakfast', 'region': 'South India', 'is_vegetarian': True, 'calories': 180, 'protein': 4.5, 'carbs': 20.0, 'fat': 8.0, 'fiber': 2.0},
    {'name': 'Rava Upma', 'category': 'Breakfast', 'region': 'South India', 'is_vegetarian': True, 'calories': 160, 'protein': 4.0, 'carbs': 25.0, 'fat': 5.0, 'fiber': 2.5},
]


class Command(BaseCommand):
    help = 'Seed the database with common Indian food items.'

    def handle(self, *args, **options):
        created = 0
        for item in FOOD_ITEMS:
            obj, _ = Food.objects.get_or_create(name=item['name'], defaults=item)
            if _:
                created += 1
        self.stdout.write(self.style.SUCCESS(f'Seeded {created} foods.'))
