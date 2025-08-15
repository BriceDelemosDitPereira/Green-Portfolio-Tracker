from django.test import TestCase # TestCase is used to create tests for Django applications
import pytest # pytest is a testing framework
from rest_framework.test import APIClient # APIClient is used to test API endpoints
from green_portfolio_tracker.api.models import Investment, PortfolioTransaction
from django.contrib.auth.models import User

@pytest.fixture # Fixture is used to create reusable test data
def client():
    return APIClient() # Fixture to provide an API client for tests

@pytest.fixture
def user(client):
    user = User.objects.create_user(username='testuser', password='testpass123')
    client.login(username='testuser', password='testpass123')
    return user

@pytest.mark.django_db # Mark the test to use the Django database (database deactivated for tests to secure isolation)
# Create only for test. The table for the test will be created and dropped after the test
def test_create_investment(client, user):
    url = '/api/investments/'
    data = {
        'name': 'Wind Farm',
        'category': 'Renewable',
        'co2_reduction_per_unit': 1.5,
        'expected_return': 5.0
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201 # assert is used to check if the condition is true
    assert Investment.objects.count() == 1
    assert Investment.objects.first().name == 'Wind Farm'