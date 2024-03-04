from django.contrib import admin

# Register your models here.
from .models import Client, Notification, Message

admin.site.register(Client)
admin.site.register(Notification)
admin.site.register(Message)
