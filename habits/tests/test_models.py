import pytest
from django.core.exceptions import ValidationError
from habits.models import Habit
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_habit_creation():
    user = User.objects.create_user(username='testuser', password='password123')
    habit = Habit.objects.create(
        creator=user,
        action='Прогулка',
        place='Парк',
        time='19:00',
        duration=60,
        frequency=1
    )
    assert habit.action == 'Прогулка'
    assert habit.duration <= 120


@pytest.mark.django_db
def test_habit_validation():
    user = User.objects.create_user(username='testuser', password='password123')
    habit = Habit(
        creator=user,
        action='Прогулка',
        place='Парк',
        time='19:00',
        duration=200,  # Ошибка валидации
        frequency=1
    )
    with pytest.raises(ValidationError):
        habit.clean()
