import os

import requests
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models


class Client(models.Model):
	phone = models.PositiveBigIntegerField(
		unique=True,
		validators=[
			MinValueValidator(70000000000),
			MaxValueValidator(79999999999),
			RegexValidator(
				regex=r'^7\d{10}$',
				message='The mobile number must have the format: 7XXXXXXXXXX',
				code='invalid_phone_number'
			),
		],
		verbose_name=' Номер телефона',
		help_text=' Номер телефона клиента в формате 7XXXXXXXXXX. Уникален для каждого клиента.',
	)
	operator_code = models.CharField(
		verbose_name='Код оператора',
		help_text='Код оператора в формате XXX. Задаётся автоматически из номера телефона.',
		max_length=3,
		validators=[
			RegexValidator(
				regex=r'^\d{3}$',
				code='invalid_mobile_code'
			),
		]
	)
	tag = models.CharField(
		max_length=255,
		verbose_name='Тег (произвольная метка)',
	)
	timezone = models.CharField(
		max_length=255,
		verbose_name='Часовой пояс',
		help_text='Часовой пояс клиента в формате "Europe/Moscow".',
	)

	def save(self, *args, **kwargs):
		self.operator_code = str(self.phone)[1:4]
		super().save(*args, **kwargs)


class Notification(models.Model):
	STATUS_CHOICES = (
		('N', 'Not Started'),
		('S', 'Started'),
		('F', 'Finished'),
	)

	date_time_start = models.DateTimeField(
		verbose_name='Дата и время начала рассылки',
	)
	date_time_stop = models.DateTimeField(
		verbose_name='Дата и время окончания рассылки',
	)
	time_interval_start = models.TimeField(
		verbose_name='Начало временного интервала', null=True, blank=True
	)
	time_interval_stop = models.TimeField(
		verbose_name='Конец временного интервала', null=True, blank=True
	)
	text = models.TextField(
		verbose_name='Текст рассылки',
	)
	tags = models.TextField(
		verbose_name='Список тэгов',
		help_text='Список тэгов для рассылки. Тэги должны быть отделены запятыми.',
	)
	status = models.CharField(
		max_length=1,
		choices=STATUS_CHOICES,
		default='N'
	)

	def send_message(self, message_id, phone):
		"""
		Отправляет сообщение на номер телефона клиент через внешний API.
		:param message_id: id сообщения
		:param phone: номер телефона клиента
		:return: Код ответа
		"""
		api_url = os.getenv('API_URL')
		url = f'{api_url}{message_id}'
		token = os.getenv('JWT_TOKEN')
		data = {"id": message_id, "phone": phone, "text": self.text}

		response = requests.post(
			url,
			json=data,
			headers={'Authorization': f'Bearer {token}'}
		)

		return response.status_code


class Message(models.Model):
	notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
	client = models.ForeignKey(Client, on_delete=models.CASCADE)
	status = models.BooleanField(
		verbose_name='Статус отправки сообщения',
		default=False,
	)
	date_time_send = models.DateTimeField(
		verbose_name='Дата и время отправки сообщения',
		auto_now=True,
	)
