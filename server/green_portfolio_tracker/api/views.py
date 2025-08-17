from rest_framework import viewsets, permissions
from django.db.models import F, FloatField
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
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return PortfolioTransaction.objects.all()

    def perform_create(self, serializer):
        serializer.save()
        cache.delete("summary_all")  # Cache pour tous les users (demo)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        cache_key = "summary_all"
        cached_result = cache.get(cache_key)
        if cached_result:
            return Response(cached_result)

        last_transaction = self.get_queryset().order_by('-date').first()
        if not last_transaction:
            result = {'total_impact': 0, 'total_performance': 0}
        else:
            total_impact = float(float(last_transaction.amount) * last_transaction.investment.co2_reduction_per_unit)
            total_performance = float(float(last_transaction.amount) * last_transaction.investment.expected_return / 100)
            result = {
                'total_impact': total_impact,
                'total_performance': total_performance
            }
        cache.set(cache_key, result, 60 * 5)
        return Response(result)