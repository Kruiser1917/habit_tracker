from rest_framework.viewsets import ModelViewSet
from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwnerOrReadOnly
from .tasks import send_habit_reminder
from rest_framework.generics import ListAPIView


class PublicHabitsView(ListAPIView):
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer


def perform_create(self, serializer):
    habit = serializer.save(creator=self.request.user)
    send_habit_reminder.apply_async((habit.id,), countdown=10)  # Отложенное выполнение через 10 секунд


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        # Публичные привычки и привычки текущего пользователя
        return Habit.objects.filter(creator=self.request.user) | Habit.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Habit.objects.filter(creator=self.request.user)
        return Habit.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
