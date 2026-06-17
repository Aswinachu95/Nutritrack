from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Food, MealLog, DietPlan, UserProfile


class FoodResource(resources.ModelResource):
    class Meta:
        model = Food
        fields = ('id', 'name', 'category', 'region', 'is_vegetarian', 'calories', 'protein', 'carbs', 'fat', 'fiber')


@admin.register(Food)
class FoodAdmin(ImportExportModelAdmin):
    resource_class = FoodResource
    list_display = ('name', 'category', 'region', 'is_vegetarian', 'calories')
    search_fields = ('name', 'category', 'region')
    list_filter = ('is_vegetarian', 'category', 'region')


@admin.register(MealLog)
class MealLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'food', 'meal_type', 'servings', 'eaten_at')
    search_fields = ('user__username', 'food__name')
    list_filter = ('meal_type',)


@admin.register(DietPlan)
class DietPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'target_calories', 'created')
    search_fields = ('name', 'user__username')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'activity_level', 'goal')
    search_fields = ('user__username',)
