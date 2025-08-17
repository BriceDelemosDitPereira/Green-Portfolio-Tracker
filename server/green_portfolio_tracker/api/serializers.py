from rest_framework import serializers
from .models import Investment, PortfolioTransaction

class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ['id', 'name', 'category', 'co2_reduction_per_unit', 'expected_return']
    
    def validate(self, data):
        if data['co2_reduction_per_unit'] < 0:
            raise serializers.ValidationError({"co2_reduction_per_unit": "Cannot be negative"})
        if data['expected_return'] < 0:
            raise serializers.ValidationError({"expected_return": "Cannot be negative"})
        return data

class PortfolioTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioTransaction
        fields = ['id', 'investment', 'amount', 'date']
        read_only_fields = ['user']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)