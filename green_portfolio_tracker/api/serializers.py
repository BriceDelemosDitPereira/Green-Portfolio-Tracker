from rest_framework import serializers
from .models import Investment, PortfolioTransaction

class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ['id', 'name', 'category', 'co2_reduction_per_unit', 'expected_return']

    def validate_co2_reduction_per_unit(self, value):
        if value < 0:
            raise serializers.ValidationError("CO2 reduction per unit must be non-negative.")
        return value

    def validate_expected_return(self, value):
        if value < 0:
            raise serializers.ValidationError("Expected return must be non-negative.")
        return value

class PortfolioTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioTransaction
        fields = ['id', 'user', 'investment', 'amount', 'date']