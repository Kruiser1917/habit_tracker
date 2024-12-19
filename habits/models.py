from django.contrib.auth.models import User
from django.db import models


class Habit(models.Model):
    objects = None
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    time = models.TimeField()
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    reward = models.CharField(max_length=255, null=True, blank=True)
    duration = models.PositiveIntegerField()  # Время выполнения в секундах
    is_public = models.BooleanField(default=False)
    frequency = models.PositiveIntegerField(default=1)  # Периодичность выполнения (дни)

    def clean(self):
        if self.related_habit and self.reward:
            raise ValidationError("Нельзя одновременно указать связанную привычку и вознаграждение.")
        if self.duration > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд.")
        if self.frequency > 7:
            raise ValidationError("Привычка должна выполняться хотя бы раз в неделю.")

    def __str__(self):
        return self.action
