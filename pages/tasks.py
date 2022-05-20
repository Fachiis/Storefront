from time import sleep
from celery import shared_task


@shared_task
def notify_customers(message):
    print("Sending 10k emails...")
    print(message)
    sleep(12)
    print("Emails were sent successfully")
