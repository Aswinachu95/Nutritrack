from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views

router = DefaultRouter()
router.register(r'foods', views.FoodViewSet)
router.register(r'meal-logs', views.MealLogViewSet)
router.register(r'plans', views.DietPlanViewSet)

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),

    # Basic UI pages (templates) for browsing data
    path('foods/', views.FoodsListView.as_view(), name='foods-list'),
    path('foods/<int:pk>/', views.FoodDetailView.as_view(), name='food-detail'),
    path('meal-logs/', views.MealLogsView.as_view(), name='meal-logs'),
    path('plans/', views.PlansView.as_view(), name='plans'),
    path('daily-summary-page/', views.DailySummaryPageView.as_view(), name='daily-summary-page'),

    path('api/', include(router.urls)),
    path('api/auth/register/', views.RegisterAPIView.as_view(), name='api-register'),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/profile/', views.UserProfileAPIView.as_view(), name='api-profile'),
    path('api/daily-summary/', views.DailySummaryView.as_view(), name='daily-summary'),

]
