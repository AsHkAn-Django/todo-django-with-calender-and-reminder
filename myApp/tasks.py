from celery import shared_task
from twilio.rest import Client
from django.conf import settings
from .models import Task

@shared_task
def send_alert_sms(task):
    message = f"Overdue Task!\n Your task {task.title}'s overdue was on {task.deadline}. Do it now!"
    client = Client(settings.MY_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    tasks = Task.objects.all()
    for task in task:
        if task.is_overdue():
            client.messages.create(to=settings.MY_PHONE_NUMBER,
                                from_=settings.MY_TWILIO_NUMBER,
                                body=message)
            print('A message was sent for an overdue task!')