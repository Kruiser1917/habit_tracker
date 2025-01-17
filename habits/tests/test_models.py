import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from habit_tracker.models import Habit  # Исправьте импорт моделей


@pytest.mark.django_db
class TestHabitModel:
    @pytest.fixture
    def user(self):
        """Создаем тестового пользователя."""
        return get_user_model().objects.create_user(username="testuser", password="password", email="test@example.com")

    def test_create_habit(self, user):
        """Проверка создания новой привычки."""
        habit = Habit.objects.create(
            creator=user,
            action="Прогулка по парку",
            place="Парк",
            time="08:00",
            is_pleasant=False,
            duration=60,
            frequency=1
        )
        assert habit.creator == user
        assert habit.action == "Прогулка по парку"
        assert habit.place == "Парк"
        assert habit.time == "08:00"
        assert habit.is_pleasant is False
        assert habit.duration == 60
        assert habit.frequency == 1

    def test_habit_invalid_duration(self, user):
        """Проверка, что время выполнения привычки больше 120 секунд вызывает ошибку валидации."""
        habit = Habit(
            creator=user,
            action="Прогулка по парку",
            place="Парк",
            time="08:00",
            is_pleasant=False,
            duration=130,  # неверное значение
            frequency=1
        )
        with pytest.raises(ValidationError):
            habit.clean()  # Вызываем чистую валидацию модели

    def test_habit_reward_and_related_habit(self, user):
        """Проверка, что нельзя указать одновременно вознаграждение и связанную привычку."""
        pleasant_habit = Habit.objects.create(
            creator=user,
            action="Чтение книги",
            place="Квартира",
            time="21:00",
            is_pleasant=True,
            duration=60,
            frequency=1
        )
        habit = Habit(
            creator=user,
            action="Прогулка по парку",
            place="Парк",
            time="08:00",
            is_pleasant=False,
            reward="Чашка кофе",
            related_habit=pleasant_habit,
            duration=60,
            frequency=1
        )
        with pytest.raises(ValidationError):
            habit.clean()

    def test_habit_related_habit_is_pleasant(self, user):
        """Проверка, что связанные привычки могут быть только с приятной привычкой."""
        habit = Habit(
            creator=user,
            action="Прогулка по парку",
            place="Парк",
            time="08:00",
            is_pleasant=False,
            reward="Чашка кофе",
            related_habit=None,
            duration=60,
            frequency=1
        )
        pleasant_habit = Habit.objects.create(
            creator=user,
            action="Прослушивание подкастов",
            place="Квартира",
            time="10:00",
            is_pleasant=True,
            duration=60,
            frequency=1
        )
        habit.related_habit = pleasant_habit
        habit.clean()  # Это должно пройти

        habit.is_pleasant = True
        habit.clean()  # Приятная привычка не может быть связана с другой

        habit.related_habit = pleasant_habit  # Убедимся, что это ошибка
        with pytest.raises(ValidationError):
            habit.clean()

    def test_pleasant_habit_no_reward_or_related_habit(self, user):
        """Проверка, что у приятной привычки не может быть вознаграждения или связанной привычки."""
        habit = Habit(
            creator=user,
            action="Просмотр сериала",
            place="Квартира",
            time="20:00",
            is_pleasant=True,
            reward="Печенье",  # Это нарушает валидацию
            related_habit=None,
            duration=60,
            frequency=1
        )
        with pytest.raises(ValidationError):
            habit.clean()

    def test_habit_frequency(self, user):
        """Проверка, что периодичность не может быть больше 7 дней."""
        habit = Habit(
            creator=user,
            action="Спортивные тренировки",
            place="Спортивный зал",
            time="06:00",
            is_pleasant=False,
            reward="Ужин с друзьями",
            duration=60,
            frequency=8  # Невозможная периодичность
        )
        with pytest.raises(ValidationError):
            habit.clean()

    def test_habit_create_without_reward_or_related_habit(self, user):
        """Проверка, что привычка может быть создана без вознаграждения и связанной привычки."""
        habit = Habit(
            creator=user,
            action="Чтение книги",
            place="Квартира",
            time="22:00",
            is_pleasant=False,
            duration=60,
            frequency=1
        )
        habit.clean()  # Это не должно вызвать ошибок

    def test_user_can_create_public_habit(self, user):
        """Проверка, что пользователь может создать публичную привычку."""
        habit = Habit.objects.create(
            creator=user,
            action="Зарядка по утрам",
            place="Квартира",
            time="07:00",
            is_pleasant=False,
            duration=10,
            frequency=1,
            is_public=True
        )
        assert habit.is_public is True

    def test_related_habit_validation(self, user):
        """Проверка, что можно добавить связанную привычку только если она является приятной."""
        habit = Habit(
            creator=user,
            action="Прогулка по парку",
            place="Парк",
            time="08:00",
            is_pleasant=False,
            duration=60,
            frequency=1
        )

        pleasant_habit = Habit.objects.create(
            creator=user,
            action="Чтение книги",
            place="Квартира",
            time="21:00",
            is_pleasant=True,
            duration=60,
            frequency=1
        )

        habit.related_habit = pleasant_habit  # Это должно работать
        habit.clean()

        habit.is_pleasant = True
        with pytest.raises(ValidationError):
            habit.clean()  # Приятная привычка не может быть связана с другой
