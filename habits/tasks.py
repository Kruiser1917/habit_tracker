from celery import shared_task
from telegram import Bot
from habit_tracker.models import Habit


@shared_task
def send_reminder(chat_id, message):
    bot = Bot(token='7480428085:AAFiSltMiRKy4zr1FhO3vwY2FMsSyj5fcjs')
    bot.send_message(chat_id=chat_id, text=message)


@shared_task
def send_habit_reminder(habit_id):
    try:
        habit = Habit.objects.get(id=habit_id)
        bot = Bot(token='YOUR_BOT_TOKEN')
        message = f"Напоминание о привычке: {habit.action} в {habit.place} в {habit.time}."
        bot.send_message(chat_id='YOUR_CHAT_ID', text=message)
    except Habit.DoesNotExist:
        pass
