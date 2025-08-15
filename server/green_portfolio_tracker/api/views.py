from rest_framework import viewsets, permissions # viewsets is used to create views that provide CRUD operations for models, and permissions are used to control access to these views. (CRUD : Create, Read, Update, Delete)
from django.db.models import F, Sum, FloatField
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.cache import cache

from .models import Investment, PortfolioTransaction
from .serializers import InvestmentSerializer, PortfolioTransactionSerializer

class InvestmentViewSet(viewsets.ModelViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PortfolioTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = PortfolioTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PortfolioTransaction.objects.filter(user=self.request.user)
    
    # @action is used to add custom actions to the viewset
    @action(detail=False, methods=['get'])
    def summary(self, request):
        cache_key = f"summary_{request.user.id}"  # Clé unique par utilisateur
        cached_result = cache.get(cache_key)
        if cached_result:
            return Response(cached_result)

        qs = self.get_queryset()
        total_impact = qs.annotate(
            impact=F('amount') * F('investment__co2_reduction_per_unit')
        ).aggregate(total_impact=Sum('impact', output_field=FloatField()))['total_impact'] or 0
        total_performance = qs.annotate(
            performance=F('amount') * F('investment__expected_return') / 100
        ).aggregate(total_performance=Sum('performance', output_field=FloatField()))['total_performance'] or 0
        result = {
            'total_impact': total_impact,
            'total_performance': total_performance
        }
        cache.set(cache_key, result, 60 * 5)  # Cache pendant 5 minutes
        return Response(result)