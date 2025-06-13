# To-Do List with Calendar Integration & Reminders

A simple to-do list application enhanced with a calendar view and automatic deadline reminders.

## Features

- Calendar integration to display tasks by date
- Email or SMS reminders for upcoming deadlines
- Toggle between list and calendar views

## Technologies Used

- Calendar library
- Notification service (SMTP)
- Backend framework (Flask, Django)

## Learning Highlights

- Calendar UI integration
- Time-based notifications
- Using third-party APIs

## Tutorial

### Integrate a calendar library to visually display tasks on a date grid

1. prepare the data for the calendar in the views.py
```python
class TaskListJson(View):
    """Returns all tasks in JSON format suitable for FullCalendar."""
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()

        events = []
        for t in tasks:
            events.append({
                'id': t.id,
                'title': t.title,
                'start': t.deadline.isoformat(),
                'allDay': False,
                'url': f'/tasks/{t.id}/',
            })

        return JsonResponse(events, safe=False)
```

2. create the url for it in urls.py
```python
    path('api/tasks/', views.TaskListJson.as_view(), name='task-list-json'),
```

3. add this to your base.html
```html
  <!-- ✅ FullCalendar v6 CSS (no separate dayGrid CSS needed in v6) -->
  <link href="https://cdn.jsdelivr.net/npm/fullcalendar@6.1.17/index.global.min.css" rel="stylesheet">

  <!-- ✅ FullCalendar v6 JS bundle with all plugins -->
  <script src="https://cdn.jsdelivr.net/npm/fullcalendar@6.1.17/index.global.min.js"></script>
```

4. add the calendar to your html
```html

<div id="calendar"></div>

<script>
  document.addEventListener("DOMContentLoaded", function () {
    const calendarEl = document.getElementById("calendar");

    const calendar = new FullCalendar.Calendar(calendarEl, {
      headerToolbar: {
        left: "prev,next today",
        center: "title",
        right: "dayGridMonth,dayGridWeek",
      },
      initialView: "dayGridMonth",
      navLinks: true,
      editable: false,
      dayMaxEvents: true,
      events: {
        url: "{% url 'myApp:task-list-json' %}",
        failure: function () {
          alert("There was an error while fetching events!");
        },
      },
    });

    calendar.render();
  });
</script>
```

### Allow users to switch between list and calendar views.
1. add this to your html
```html
  <h3 class="text-center mb-4 text-success">Switch between List and Calendar</h3>
  <ul class="nav nav-tabs mb-3" id="taskTabs" role="tablist">
    <li class="nav-item" role="presentation">
      <button class="nav-link active" id="list-tab" data-bs-toggle="tab" data-bs-target="#list" type="button" role="tab">List</button>
    </li>
    <li class="nav-item" role="presentation">
      <button class="nav-link" id="calendar-tab" data-bs-toggle="tab" data-bs-target="#calendar" type="button" role="tab">Calendar</button>
    </li>
  </ul>
```

### Implement email or SMS reminders for upcoming deadlines.
1. first add the redis and twilio config in your settings( I used whatsapp version for twilio because it was easier to run without country problem )
```python
# Twilio settings
MY_ACCOUNT_SID = config("MY_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")
MY_TWILIO_NUMBER = config("MY_TWILIO_NUMBER")
MY_PHONE_NUMBER =config("MY_PHONE_NUMBER")


# Use Redis as broker and backend
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
```

2. celery.py
```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toDoList.settings')
app = Celery('toDoList')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
app.conf.timezone = 'UTC'
app.autodiscover_tasks()
```

3. __ init __.py
```python
from .celery import app as celery_app

__all__ = ("celery_app",)
```

4. tasks.py
```python
from celery import shared_task
from twilio.rest import Client
from django.conf import settings
from .models import Task

@shared_task
def send_alert_sms():
    client = Client(settings.MY_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    tasks = Task.objects.all()
    for task in tasks:
        message = f"Overdue Task!\nYour task '{task.title}' was due on {task.deadline}. Do it now!"
        if task.is_overdue():
            client.messages.create(
                to=settings.MY_PHONE_NUMBER,
                from_=settings.MY_TWILIO_NUMBER,
                body=message
            )
            print(f"✅ Sent SMS for task: {task.title}")
```

5. open 4 terminals and run
```shell
python manage.py runserver
```
```shell
redis-server
# if you get error
# sudo systemctl stop redis
# still error?
# find out the port is busy by what
#lsof -i :6379
# then kill it
#kill -9 <PID>
```
```shell
celery -A toDoList worker --loglevel=info
```
```shell
celery -A toDoList beat --loglevel=info
```

FINISHED :)