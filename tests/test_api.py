import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_habit_creation():
    client = APIClient()
    response = client.post('/api/habits/', data={
        'action': 'Прогулка',
        'place': 'Парк',
        'time': '19:00',
        'duration': 120,
        'frequency': 1
    })
    assert response.status_code == 201
