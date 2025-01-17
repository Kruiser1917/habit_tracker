from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


# Кастомная модель пользователя
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Email обязателен и уникален

    def __str__(self):
        return self.username


# Модель привычек
class Habit(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="habits")
    action = models.CharField(max_length=255, verbose_name="Действие")
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    related_habit = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Связанная привычка", related_name="related_to"
    )
    reward = models.CharField(max_length=255, null=True, blank=True, verbose_name="Вознаграждение")
    duration = models.PositiveIntegerField(verbose_name="Время выполнения (в секундах)")
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")
    frequency = models.PositiveIntegerField(default=1, verbose_name="Периодичность (дни)")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def clean(self):
        # Проверка: Нельзя одновременно указать вознаграждение и связанную привычку
        if self.reward and self.related_habit:
            raise ValidationError("Нельзя одновременно указать вознаграждение и связанную привычку.")

        # Проверка: Время выполнения ≤ 120 секунд
        if self.duration > 120:
            raise ValidationError("Время выполнения привычки не может превышать 120 секунд.")

        # Проверка: Периодичность не реже, чем раз в 7 дней
        if self.frequency > 7:
            raise ValidationError("Привычка должна выполняться хотя бы раз в неделю (максимум 7 дней между "
                                  "повторениями).")

        # Проверка: Связанные привычки должны быть только с признаком приятной привычки
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("В связанные привычки могут попадать только привычки с признаком приятной привычки.")

        # Проверка: Приятная привычка не может иметь связанной привычки или вознаграждения
        if self.is_pleasant and (self.related_habit or self.reward):
            raise ValidationError("Приятная привычка не может иметь связанной привычки или вознаграждения.")

    def __str__(self):
        return self.action
