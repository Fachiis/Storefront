# from django.http import HttpResponse
import requests
import logging
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView

# with the magic __name__, it will translate to  a log bucket -> pages.views
logger = logging.getLogger(__name__)

# from django.core.cache import cache

# from django.conf import settings
# from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
# from templated_mail.mail import BaseEmailMessage

# from .tasks import notify_customers

# Decorate a function view with cache with timeout
# @cache_page(5 * 10)
# def index(request):
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
# notify_customers.delay("Hello You")

# key = "httpbin_result"
# if cache.get(key) is None:
#     response = requests.get("https://httpbin.org/delay/2")
#     data = response.json()
#     cache.set(key, data)

# response = requests.get("https://httpbin.org/delay/2")
# data = response.json()

# return render(request, "home.html", {"name": data})


class Index(APIView):
    # @method_decorator(cache_page(5 * 60))
    def get(self, request):
        try:
            logger.info("Request sent to http bin")
            response = requests.get("https://httpbin.org/delay/2")
            logger.info("Response received from http bin")
            data = response.json()
        except requests.ConnectionError:
            logger.critical("http bin server is offline")

        return render(request, "home.html", {"name": data})
