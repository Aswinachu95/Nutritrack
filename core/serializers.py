from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Food, MealLog, DietPlan, UserProfile

User = get_user_model()


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    bmr = serializers.ReadOnlyField()
    target_calories = serializers.ReadOnlyField()
    target_protein_g = serializers.ReadOnlyField()
    target_carbs_g = serializers.ReadOnlyField()
    target_fat_g = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        fields = [
            'age',
            'gender',
            'height_cm',
            'weight_kg',
            'activity_level',
            'goal',
            'bmr',
            'target_calories',
            'target_protein_g',
            'target_carbs_g',
            'target_fat_g',
        ]


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
