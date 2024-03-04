import random

from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Client, Notification, Message

client = APIClient()
User = get_user_model()


class ClientTest(APITestCase):
	def setUp(self) -> None:
		self.superuser = User.objects.create_superuser(
			'admin',
			password='Pas$w0rd',
		)

		self.client.force_authenticate(self.superuser)

		for number in range(random.randint(1, 10)):
			baker.make(Client)

		self.client_obj = Client.objects.order_by('?').first()

	def test_clients_operator_code(self):
		client = baker.make(Client, phone=79991111111)
		self.assertEqual(client.operator_code, '999')

	def test_clients_list_anon(self):
		self.client.logout()

		url = reverse('client-list')
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_clients_list(self):
		url = reverse('client-list')
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_clients_create(self):
		url = reverse('client-list')
		response = self.client.post(url, data={'phone': 79991111111, 'tag': 'tag1',
		                                       'timezone': 'America/Argentina/Buenos_Aires'})

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_clients_detail(self):
		url = reverse('client-detail', args=[self.client_obj.id])
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_clients_update(self):
		url = reverse('client-detail', args=[self.client_obj.id])
		response = self.client.patch(url, data={'tag': 'tag2'})

		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_clients_delete(self):
		url = reverse('client-detail', args=[self.client_obj.id])
		response = self.client.delete(url)

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class NotificationTest(APITestCase):
	def setUp(self) -> None:
		self.superuser = User.objects.create_superuser(
			'admin',
			password='Pas$w0rd',
		)

		self.client.force_authenticate(self.superuser)

		for number in range(random.randint(1, 10)):
			baker.make(Notification)

		for number in range(random.randint(1, 10)):
			baker.make(Message)

		self.notification = Notification.objects.order_by('?').first()

		self.messages_sended = Message.objects.filter(notification=self.notification, status=True).count()
		self.messages_not_sended = Message.objects.filter(notification=self.notification, status=False).count()

		self.total_notifications = Notification.objects.count()
		self.total_messages_sended = Message.objects.filter(status=True).count()
		self.total_messages_not_sended = Message.objects.filter(status=False).count()

		self.date = self.notification.date_time_start.date()

		self.date_total_notifications = Notification.objects.filter(date_time_start__date=self.date).count()
		self.date_total_messages_sended = Message.objects.filter(notification__date_time_start__date=self.date,
		                                                         status=True).count()
		self.date_total_messages_not_sended = Message.objects.filter(notification__date_time_start__date=self.date,
		                                                             status=False).count()

	def test_notifications_list(self):
		url = reverse('notification-list')
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_notifications_detail(self):
		url = reverse('notification-detail', args=[self.notification.id])
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['messages_sended'], self.messages_sended)
		self.assertEqual(response.data['messages_not_sended'], self.messages_not_sended)

	def test_notifications_statistic(self):
		url = reverse('notification-statistics')
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['total_notifications'], self.total_notifications)
		self.assertEqual(response.data['total_messages_sended'], self.total_messages_sended)
		self.assertEqual(response.data['total_messages_not_sended'], self.total_messages_not_sended)

	def test_notifications_statistic_date(self):
		url = reverse('notification-statistics-date', args=[self.date])
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)

		self.assertEqual(response.data['total_notifications'], self.date_total_notifications)
		self.assertEqual(response.data['total_messages_sended'], self.date_total_messages_sended)
		self.assertEqual(response.data['total_messages_not_sended'], self.date_total_messages_not_sended)

	def test_notifications_create(self):
		url = reverse('notification-list')
		data = {'date_time_start': '2022-11-11+11:11', 'date_time_stop': '2022-11-12+11:11', 'text': 'text',
		        'tags': ['tag1', 'tag2']}
		response = self.client.post(url, data=data)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_notifications_update(self):
		url = reverse('notification-detail', args=[self.notification.id])
		response = self.client.patch(url, data={'text': 'text'})

		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_notifications_delete(self):
		url = reverse('notification-detail', args=[self.notification.id])
		response = self.client.delete(url)

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class MessageTest(APITestCase):
	def setUp(self) -> None:
		self.superuser = User.objects.create_superuser(
			'admin',
			password='Pas$w0rd',
		)

		self.client.force_authenticate(self.superuser)

		for number in range(random.randint(1, 10)):
			baker.make(Notification)

		for number in range(random.randint(1, 10)):
			baker.make(Message)

		self.client_obj = Client.objects.order_by('?').first()
		self.notification = Notification.objects.order_by('?').first()
		self.message = Message.objects.order_by('?').first()

	def test_clients_list(self):
		url = reverse('message-list')
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_clients_create(self):
		url = reverse('message-list')
		data = {'notification': self.notification.id, 'client': self.client_obj.id}
		response = self.client.post(url, data=data)

		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

	def test_clients_detail(self):
		url = reverse('message-detail', args=[self.message.id])
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_clients_update(self):
		url = reverse('message-detail', args=[self.message.id])
		response = self.client.patch(url, data={'status': True})

		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

	def test_clients_delete(self):
		url = reverse('message-detail', args=[self.message.id])
		response = self.client.delete(url)

		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
