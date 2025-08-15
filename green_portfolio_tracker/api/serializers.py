from rest_framework import serializers # Serializers is used to convert complex data types, like querysets and model instances, into native Python datatypes that can then be easily rendered into JSON or XML.
from .models import Investment, PortfolioTransaction

class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = '__all__'

class PortfolioTransactionSerializer(serializers.ModelSerializer):
    impact = serializers.ReadOnlyField(source='calculate_impact')
    performance = serializers.ReadOnlyField(source='calculate_performance')

    class Meta:
        model = PortfolioTransaction
        fields =  ['id', 'investment', 'amount', 'date', 'impact', 'performance']