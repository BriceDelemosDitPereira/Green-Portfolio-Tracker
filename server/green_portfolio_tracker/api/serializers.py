from rest_framework import serializers
from .models import Investment, PortfolioTransaction

class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ['id', 'name', 'category', 'co2_reduction_per_unit', 'expected_return']

class PortfolioTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioTransaction
        fields = ['id', 'investment', 'amount', 'date']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)