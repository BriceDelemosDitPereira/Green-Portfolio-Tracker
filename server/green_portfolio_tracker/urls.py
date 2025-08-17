from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from rest_framework.routers import DefaultRouter
from green_portfolio_tracker.api.views import InvestmentViewSet, PortfolioTransactionViewSet

# Create a router and register our viewsets with it.
# This will automatically create the URL patterns for the viewsets.
router = DefaultRouter()
router.register(r'investments', InvestmentViewSet)
router.register(r'transactions', PortfolioTransactionViewSet, basename='transactions')

def redirect_to_api(request):
    return HttpResponseRedirect('/api/')

urlpatterns = [
    path('', redirect_to_api, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]