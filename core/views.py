from rest_framework import viewsets, generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, F

from .models import Food, MealLog, DietPlan
from .serializers import FoodSerializer, MealLogSerializer, DietPlanSerializer


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'region', 'is_vegetarian']
    search_fields = ['name', 'category', 'region']
    ordering_fields = ['calories', 'protein', 'carbs', 'fat']


class MealLogViewSet(viewsets.ModelViewSet):
    serializer_class = MealLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MealLog.objects.filter(user=self.request.user).select_related('food')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DietPlanViewSet(viewsets.ModelViewSet):
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
