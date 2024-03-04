from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from .models import Client, Notification, Message


class ClientSerializer(serializers.ModelSerializer):
	timezone = TimeZoneSerializerField(use_pytz=True)

	class Meta:
		model = Client
		fields = ('id', 'phone', 'operator_code', 'tag', 'timezone',)
		read_only_fields = ('operator_code',)


class NotificationSerializer(serializers.ModelSerializer):
	messages_sended = serializers.IntegerField(
		read_only=True,
		label='Количество отправленных сообщений рассылкой',
	)
	messages_not_sended = serializers.IntegerField(
		read_only=True,
		label='Количество сообщений, отправка которых завершилось ошибкой'
	)

	class Meta:
		model = Notification
		fields = ('id', 'date_time_start', 'date_time_stop', 'time_interval_start', 'time_interval_stop', 'text', 'tags', 'messages_sended', 'messages_not_sended',)
		read_only_fields = ('messages_sended', 'messages_not_sended',)


class MessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = ('id', 'notification', 'client', 'status', 'date_time_send',)
