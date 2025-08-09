from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_reminder_email(child_user_id, task_description):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.get(id=child_user_id)
    send_mail(
        'Reminder: Task Pending',
        f'Hi {user.username}, remember to complete: {task_description}',
        'noreply@yourapp.com',
        [user.email],
        fail_silently=False,
    )
