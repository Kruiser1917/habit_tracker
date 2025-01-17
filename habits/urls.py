from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet
from .views import PublicHabitsView

router = DefaultRouter()
router.register(r'habits', HabitViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/public-habits/', PublicHabitsView.as_view(), name='public-habits'),
]
