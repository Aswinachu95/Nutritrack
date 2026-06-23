from rest_framework import serializers
from .models import Food, MealLog, DietPlan


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class MealLogSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)
    food_id = serializers.PrimaryKeyRelatedField(queryset=Food.objects.all(), write_only=True, source='food')
    calories_total = serializers.FloatField(read_only=True)

    class Meta:
        model = MealLog
        fields = ['id', 'user', 'food', 'food_id', 'servings', 'meal_type', 'eaten_at', 'calories_total']
        read_only_fields = ['user']


class DietPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietPlan
        fields = '__all__'
        read_only_fields = ['user', 'created']
