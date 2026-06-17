
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, UpdateView

from rest_framework import viewsets, generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, F

from .forms import UserRegistrationForm, UserProfileForm, MealLogForm, DietPlanForm
from .models import Food, MealLog, DietPlan, UserProfile
from .serializers import (
    FoodSerializer,
    MealLogSerializer,
    DietPlanSerializer,
    RegisterSerializer,
    ProfileSerializer,
)


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'region', 'is_vegetarian']
    search_fields = ['name', 'category', 'region']
    ordering_fields = ['calories', 'protein', 'carbs', 'fat']


class MealLogViewSet(viewsets.ModelViewSet):
    queryset = MealLog.objects.all()
    serializer_class = MealLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MealLog.objects.filter(user=self.request.user).select_related('food')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DietPlanViewSet(viewsets.ModelViewSet):
    queryset = DietPlan.objects.all()
    serializer_class = DietPlanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DietPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DailySummaryView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date = request.query_params.get('date')
        if not date:
            return Response({'detail': 'date param required (YYYY-MM-DD)'}, status=400)

        qs = MealLog.objects.filter(user=request.user, eaten_at=date).aggregate(
            calories=Sum(F('servings') * F('food__calories')),
            protein=Sum(F('servings') * F('food__protein')),
            carbs=Sum(F('servings') * F('food__carbs')),
            fat=Sum(F('servings') * F('food__fat')),
        )
        return Response(qs)


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class HomeView(TemplateView):
    template_name = 'core/home.html'


class RegisterView(FormView):
    template_name = 'core/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'core/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class FoodsListView(TemplateView):
    template_name = 'core/foods_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['foods'] = Food.objects.all().order_by('name')
        return ctx


class FoodDetailView(TemplateView):
    template_name = 'core/food_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        ctx['food'] = Food.objects.filter(pk=pk).first()
        return ctx


class MealLogsView(LoginRequiredMixin, TemplateView):
    template_name = 'core/meal_logs.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['meal_logs'] = MealLog.objects.filter(user=self.request.user).select_related('food').order_by('-eaten_at')
        ctx['form'] = MealLogForm()
        return ctx

    def post(self, request, *args, **kwargs):
        form = MealLogForm(request.POST)
        if form.is_valid():
            ml = form.save(commit=False)
            ml.user = request.user
            ml.save()
            return redirect('meal-logs')
        ctx = self.get_context_data()
        ctx['form'] = form
        return self.render_to_response(ctx)


class PlansView(LoginRequiredMixin, TemplateView):
    template_name = 'core/plans.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['plans'] = DietPlan.objects.filter(user=self.request.user).order_by('-created')
        ctx['form'] = DietPlanForm()
        return ctx

    def post(self, request, *args, **kwargs):
        form = DietPlanForm(request.POST)
        if form.is_valid():
            dp = form.save(commit=False)
            dp.user = request.user
            dp.save()
            return redirect('plans')
        ctx = self.get_context_data()
        ctx['form'] = form
        return self.render_to_response(ctx)


class DailySummaryPageView(LoginRequiredMixin, TemplateView):
    template_name = 'core/daily_summary.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        date = self.request.GET.get('date')
        ctx['selected_date'] = date
        if date:
            qs = MealLog.objects.filter(user=self.request.user, eaten_at=date).aggregate(
                calories=Sum(F('servings') * F('food__calories')),
                protein=Sum(F('servings') * F('food__protein')),
                carbs=Sum(F('servings') * F('food__carbs')),
                fat=Sum(F('servings') * F('food__fat')),
            )
            ctx.update(qs)
        return ctx
