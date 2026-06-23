from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'foods', views.FoodViewSet)
router.register(r'meal-logs', views.MealLogViewSet)
router.register(r'plans', views.DietPlanViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework_simplejwt.urls')),
    path('daily-summary/', views.DailySummaryView.as_view(), name='daily-summary'),
]
