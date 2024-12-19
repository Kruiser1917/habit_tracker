import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from habits.models import Habit


@pytest.mark.django_db
def test_habit_list():
    user = User.objects.create_user(username='testuser', password='password123')
    client = APIClient()
    client.login(username='testuser', password='password123')

    Habit.objects.create(
        creator=user,
        action='Прогулка',
        place='Парк',
        time='19:00',
        duration=60,
        frequency=1
    )

    response = client.get('/api/habits/')
    assert response.status_code == 200
    assert len(response.json()['results']) == 1
