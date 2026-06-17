from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'gender', 'height_cm', 'weight_kg', 'activity_level', 'goal']
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'activity_level': forms.Select(attrs={'class': 'form-select'}),
            'goal': forms.Select(attrs={'class': 'form-select'}),
        }


from .models import MealLog, DietPlan, Food


class MealLogForm(forms.ModelForm):
    class Meta:
        model = MealLog
        fields = ['food', 'servings', 'meal_type', 'eaten_at']
        widgets = {
            'food': forms.Select(attrs={'class': 'form-select'}),
            'servings': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0.1'}),
            'meal_type': forms.Select(attrs={'class': 'form-select'}),
            'eaten_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['food'].queryset = Food.objects.all().order_by('name')


class DietPlanForm(forms.ModelForm):
    class Meta:
        model = DietPlan
        fields = ['name', 'target_calories']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'target_calories': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),
        }

