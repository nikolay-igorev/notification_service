import django_filters.rest_framework as filters

from .models import Notification


class NotificationFilterSet(filters.FilterSet):
	date_time_start = filters.DateFilter(label='date_time_start', lookup_expr='date')

	class Meta:
		model = Notification
		fields = ['date_time_start', ]
