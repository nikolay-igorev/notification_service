from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Sum, Case, When, IntegerField, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from .filters import NotificationFilterSet
from .models import Client, Notification, Message
from . import schemas
from .serializers import ClientSerializer, NotificationSerializer, MessageSerializer

User = get_user_model()


@schemas.client_schema_view
class ClientViewSet(viewsets.ModelViewSet):
	serializer_class = ClientSerializer
	queryset = Client.objects.all()


@schemas.notification_schema_view
class NotificationViewSet(viewsets.ModelViewSet):
	serializer_class = NotificationSerializer
	filter_backends = (DjangoFilterBackend, OrderingFilter)
	filterset_class = NotificationFilterSet
	ordering_fields = ('messages_sended', 'messages_not_sended', 'date_time_start', 'date_time_stop')
	queryset = Notification.objects.annotate(
		messages_sended=Sum(Case(When(message__status=True, then=1),
		                         output_field=IntegerField()), default=0),
		messages_not_sended=Sum(Case(When(message__status=False, then=1),
		                             output_field=IntegerField()), default=0)

	).order_by('id')

	@schemas.notification_statistics_schema
	@action(["get"], detail=False)
	def statistics(self, request, *args, **kwargs):
		queryset = Notification.objects.aggregate(total_notifications=Count('id'),
		                                          total_messages_sended=Sum(Case(When(message__status=True, then=1),
		                                                                         output_field=IntegerField()),
		                                                                    default=0),
		                                          total_messages_not_sended=Sum(
			                                          Case(When(message__status=False, then=1),
			                                               output_field=IntegerField()), default=0)
		                                          )
		return Response(queryset)

	@schemas.notification_statistics_date_schema
	@action(["get"], detail=False, url_path='statistics/(?P<date>[A-Za-z0-9\-]+)')
	def statistics_date(self, request, *args, **kwargs):
		try:
			queryset = {'date': kwargs['date']}
			queryset.update(Notification.objects.filter(date_time_start__date=kwargs['date']).aggregate(
				total_notifications=Count('id'),
				total_messages_sended=Sum(Case(When(message__status=True, then=1),
				                               output_field=IntegerField()), default=0),
				total_messages_not_sended=Sum(Case(When(message__status=False, then=1),
				                                   output_field=IntegerField()), default=0)
			))
			return Response(queryset)
		except ValidationError:
			return Response(status=status.HTTP_404_NOT_FOUND)


@schemas.message_schema_view
class MessageViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
	serializer_class = MessageSerializer
	queryset = Message.objects.all()
	filter_backends = (DjangoFilterBackend, OrderingFilter)
	filterset_fields = ('notification',)
	ordering_fields = ('date_time_send', )
