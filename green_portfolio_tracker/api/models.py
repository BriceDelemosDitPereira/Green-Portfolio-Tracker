from django.db import models # models is used to define database models
from django.contrib.auth.models import User # User model for authentication

class Investment(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    co2_reduction_per_unit = models.FloatField(default=0.0)
    expected_return = models.FloatField(default=0.0)

    def __str__(self): # Print the name of the investment
        return self.name

class PortfolioTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def calculate_impact(self):
        return self.amount * self.investment.co2_reduction_per_unit
    
    def calculate_performance(self):
        return self.amount * (self.investment.expected_return / 100)
    
    def __str__(self): # Print the portfolio details
        return f"{self.user.username} - {self.investment.name} - {self.amount}"