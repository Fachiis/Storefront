from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from templated_mail.mail import BaseEmailMessage

from .tasks import notify_customers


def index(request):
    # try:
    # send_mail(
    #     subject="Glad you are here",
    #     message="Thank you for subscribing to our newsletter",
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     recipient_list=["dorathy@gamil.com"],
    # )
    # mail_admins(
    #     subject="Customer group created",
    #     message="Accept the respective roles in the admin section",
    #     html_message="Accept the respective roles in the admin section",
    # )
    # message = EmailMessage(
    #     subject="Logo Sent",
    #     body="The logo for the project is in the attached file.",
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     to=["dorathy@yahoo.com"],
    # )
    # message.attach_file("pages/static/images/deykam_logo.png")
    # message.send()
    #     message = BaseEmailMessage(
    #         template_name="email/email.html", context={"name": "Dorathy"}
    #     )
    #     message.send(to=["dorathy@hotmail.com"])
    # except BadHeaderError:
    #     return HttpResponse("Invalid header found.")
    notify_customers.delay("Hello You")
    return render(request, "home.html", {"name": "Fachiis"})
