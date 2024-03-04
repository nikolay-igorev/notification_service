from datetime import datetime, timedelta
from smtplib import SMTPException

import pytz
from celery import shared_task
from celery.worker.control import revoke
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status

from notification_service_project.celery import app
from .exceptions import BadRequestException
from .models import Notification, Client, Message


@shared_task
def send_messages():
	"""
	Celery задача для запуска рассылок.
	"""
	notifications = Notification.objects.filter(
		date_time_start__lte=timezone.now(),
		date_time_stop__gte=timezone.now(),
		status='N'
	)

	if notifications.exists():
		for notification in notifications:
			notification.status = 'S'
			notification.save()

		for notification in notifications:
			if notification.date_time_stop < timezone.now():
				break

			if notification.status == 'S':
				tags = notification.tags.split(',')
				clients = Client.objects.filter(
					Q(tag__in=tags) | Q(operator_code__in=tags)
				)

				for client in clients:
					if notification.time_interval_start:

						time_interval_start = notification.time_interval_start.strftime('%H:%M:%S')
						time_interval_stop = notification.time_interval_stop.strftime('%H:%M:%S')
						client_time = datetime.now(pytz.timezone(client.timezone)).strftime('%H:%M:%S')

						if time_interval_stop >= client_time > time_interval_start:
							break

					send_message.delay(notification.id, client.id)

			notification.status = 'F'
			notification.save()


@app.task(bind=True)
def send_message(self, notification_id, client_id):
	"""
	Задача для отправки сообщения клиенту.
	Если сообщение не отправилось, то до времени окончания рассылки
	попытки отправления сообщения будут повторяться.
	:param self:
	:param client_id: ID клиента
	:param notification_id: ID рассылки
	:return: None
	"""
	notification = get_object_or_404(Notification, id=notification_id)
	client = get_object_or_404(Client, id=client_id)

	if notification.date_time_stop < timezone.now():
		revoke(self.request.id, terminate=True)

	if not Message.objects.filter(notification=notification, client=client, status=True).exists():
		message, _ = Message.objects.get_or_create(
			client_id=client_id,
			notification_id=notification_id,
		)

		try:
			message_status = notification.send_message(message.id, client.phone)

			if message_status == status.HTTP_200_OK:
				message.status = True
				message.save()

			else:
				raise BadRequestException

		except BadRequestException as http_400:
			raise self.retry(exc=http_400)


@app.task(bind=True, autoretry_for=(SMTPException,))
def send_daily_email(self):
	"""
	Ежедневная задача для отправки статистики рассылок
	"""
	yesterday = (timezone.now() - timedelta(days=1))

	total_notifications = Notification.objects.filter(date_time_start__day=yesterday.day)
	total_messages_sended = Message.objects.filter(notification__in=total_notifications, status=True).count()
	total_messages_not_sended = Message.objects.filter(notification__in=total_notifications, status=False).count()

	message = f'''
	{yesterday.strftime("%Y-%m-%d")}.
	Общее количество рассылок: {total_notifications.count()};
	Общее количество отправленных сообщений: {total_messages_sended};
	Общее количество неотправленных сообщений: {total_messages_not_sended}.
	'''

	send_mail(
		f'Статистика за {yesterday.strftime("%Y-%m-%d")}',
		message,
		'admin@admin.com',
		['example@example.com'],
		fail_silently=False,
	)
