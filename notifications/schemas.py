from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, extend_schema_view, OpenApiResponse, extend_schema, OpenApiParameter

from notifications.serializers import ClientSerializer, NotificationSerializer, MessageSerializer

client_request_example = OpenApiExample(
	'Example',
	value={
		"phone": 79999999999,
		"tag": "tag1",
		"timezone": "Europe/Moscow"
	},
	request_only=True,
	response_only=False,
)

client_response_example = OpenApiExample(
	'Example',
	value={
		"id": 1,
		"phone": 79999999999,
		"operator_code": "999",
		"tag": "tag1",
		"timezone": "Europe/Moscow",
	},
	request_only=False,
	response_only=True,
)

client_schema_view = extend_schema_view(
	list=extend_schema(
		summary='Список клиентов',
		responses={
			200: OpenApiResponse(response=ClientSerializer,
			                     description='Успешная операция',
			                     examples=[client_response_example, ]
			                     ),
		},
	),

	create=extend_schema(
		summary='Добавление нового клиента в справочник',
		responses={
			201: OpenApiResponse(response=ClientSerializer,
			                     description='Успешная операция',
			                     examples=[client_response_example, ]
			                     ),
			400: OpenApiResponse(description='Некорректный запрос'),
		},
		examples=[client_request_example, ]
	),

	retrieve=extend_schema(
		summary='Нахождение клиента по ID',
		parameters=[
			OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, description='ID клиента'),
		],
		responses={
			200: OpenApiResponse(response=ClientSerializer,
			                     description='Успешная операция',
			                     examples=[client_response_example, ]),

			404: OpenApiResponse(description='Клиент с заданным ID не найден'),
		},

	),

	update=extend_schema(
		summary='Обновление существующего клиента по ID',
		parameters=[
			OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, description='ID клиента'),
		],
		responses={
			201: OpenApiResponse(response=ClientSerializer,
			                     description='Успешная операция',
			                     examples=[client_response_example, ]
			                     ),
			400: OpenApiResponse(description='Некорректный запрос'),
			404: OpenApiResponse(description='Клиент с заданным ID не найден'),
		},
		examples=[client_request_example, ]
	),

	destroy=extend_schema(
		summary='Удаление клиента по ID',
		parameters=[
			OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, description='ID клиента'),
		],
		responses={
			204: OpenApiResponse(response=ClientSerializer,
			                     description='Успешная операция',
			                     examples=[client_response_example, ]
			                     ),
			404: OpenApiResponse(description='Клиент с заданным ID не найден'),
		},
	),

	partial_update=extend_schema(methods=['PATCH'], exclude=True),

)

notification_response_example = OpenApiExample(
	'Example',
	value={
		"id": 1,
		"date_time_start": "2022-11-11T11:11:11+03:00",
		"date_time_stop": "2022-11-11T11:11:11+03:00",
		"text": "text",
		"tags": "tag1,tag2",
		"messages_sended": 0,
		"messages_not_sended": 0
	},
	request_only=False,
	response_only=True,
)

notification_request_example = OpenApiExample(
	'Example',
	value={
		"date_time_start": "2022-11-11T11:11:11+03:00",
		"date_time_stop": "2022-11-11T11:11:11+03:00",
		"text": "text",
		"tags": "tag1,tag2"
	},
	request_only=True,
	response_only=False,
)

notification_schema_view = extend_schema_view(
	list=extend_schema(
		summary='Список рассылок',
		description='Список рассылок. Содержит общее количество отправленных и неотправленных каждой рассылкой '
		            'сообщений. Для получения статистики список можно отсортировать по дате начала рассылки, '
		            'окончания рассылки, отправленным сообщениям, неотправленным сообщениям; отфильтровать по дате '
		            'начала рассылок.',
		parameters=[
			OpenApiParameter(
				name='date_time_start',
				description='Фильтр по дате начала рассылки',
				required=False,
				type=OpenApiTypes.DATE,
				location=OpenApiParameter.QUERY,
				examples=[
					OpenApiExample(
						'Example',
						value='2022-11-11'
					),
				]
			),
			OpenApiParameter(
				name='ordering',
				description='Сортировка списка рассылок. Доступные поля: date_time_start, date_time_stop, '
				            'messages_sended, messages_not_sended',
				required=False,
				type=OpenApiTypes.STR,
				location=OpenApiParameter.QUERY,
			),

		],
		responses={
			200: OpenApiResponse(response=NotificationSerializer,
			                     description='Успешная операция',
			                     examples=[notification_response_example, ]
			                     ),
		},
	),

	create=extend_schema(
		summary='Создание рассылки',
		responses={
			201: OpenApiResponse(response=NotificationSerializer,
			                     description='Успешная операция',
			                     examples=[notification_response_example, ]
			                     ),
			400: OpenApiResponse(description='Некорректный запрос'),
		},
		examples=[notification_request_example, ]
	),

	retrieve=extend_schema(
		summary='Нахождение рассылки по ID',
		description='Содержит информацию о отправленных и неотправленных рассылкой сообщений.',
		parameters=[
			OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, description='ID рассылки'),
		],
		responses={
			200: OpenApiResponse(response=NotificationSerializer,
			                     description='Успешная операция',
			                     examples=[notification_response_example, ]),

			404: OpenApiResponse(description='Рассылка с заданным ID не найдена'),
		},

	),

	update=extend_schema(
		summary='Обновление существующей рассылки по ID',
		parameters=[
			OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, description='ID рассылки'),
		],
		responses={
			201: OpenApiResponse(response=NotificationSerializer,
			                     description='Успешная операция',
			                     examples=[notification_response_example, ]
			                     ),
			400: OpenApiResponse(description='Некорректный запрос'),
			404: OpenApiResponse(description='Рассылка с заданным ID не найдена'),
		},
		examples=[notification_request_example, ]
	),

	destroy=extend_schema(
		summary='Удаление рассылки по ID',
		parameters=[
			OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, description='ID рассылки'),
		],
		responses={
			204: OpenApiResponse(response=NotificationSerializer,
			                     description='Успешная операция',
			                     examples=[notification_response_example, ]
			                     ),
			404: OpenApiResponse(description='Рассылка с заданным ID не найдена'),
		},
	),

	partial_update=extend_schema(methods=['PATCH'], exclude=True),

)

notification_statistics_schema = extend_schema(
	summary='Статистика рассылок',
	description='Отображает общее количество рассылок, отправленных и неотправленных сообщений.',
	responses={
		200: OpenApiResponse(response=NotificationSerializer,
		                     description='Успешная операция',
		                     examples=[OpenApiExample(
			                     'Example',
			                     value={
				                     "total_notifications": 0,
				                     "total_messages_sended": 0,
				                     "total_messages_not_sended": 0
			                     }
		                     )],
		                     ),
	},
)

notification_statistics_date_schema = extend_schema(
	summary='Статистика рассылок за определённый день',
	description='Отображает общее количество рассылок, отправленных и неотправленных сообщений за определённый день.',
	parameters=[
		OpenApiParameter(
			name='date',
			description='Дата начала рассылок',
			required=True,
			type=OpenApiTypes.DATE,
			location=OpenApiParameter.PATH,
			examples=[
				OpenApiExample(
					'Example',
					value='2022-11-11'
				),
			]
		),
	],
	responses={
		200: OpenApiResponse(response=NotificationSerializer,
		                     description='Успешная операция',
		                     examples=[OpenApiExample(
			                     'Example',
			                     value={
				                     "total_notifications": 0,
				                     "total_messages_sended": 0,
				                     "total_messages_not_sended": 0
			                     }
		                     )],
		                     ),
	},
)

message_response_example = OpenApiExample(
	'Example',
	value={
		"id": 1,
		"notification": 1,
		"client": 1,
		"status": True,
		"date_time_send": "2022-11-11T11:11:11+03:00"
	},
	request_only=False,
	response_only=True,
)

message_schema_view = extend_schema_view(
	list=extend_schema(
		summary='Список сообщений',
		parameters=[
			OpenApiParameter(
				name='notification',
				description=' Фильтр по ID рассылки',
				required=False,
				type=OpenApiTypes.INT,
				location=OpenApiParameter.QUERY,
			),
			OpenApiParameter(
				name='ordering',
				description='Сортировка списка сообщений. Доступные поля: date_time_send',
				required=False,
				type=OpenApiTypes.STR,
				location=OpenApiParameter.QUERY,
			),

		],
		responses={
			200: OpenApiResponse(response=MessageSerializer,
			                     description='Успешная операция',
			                     examples=[message_response_example, ]
			                     ),
		},
	),

	retrieve=extend_schema(
		summary='Нахождение сообщения по ID',
		parameters=[
			OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH, description='ID сообщения'),
		],
		responses={
			200: OpenApiResponse(response=MessageSerializer,
			                     description='Успешная операция',
			                     examples=[message_response_example, ]),

			404: OpenApiResponse(description='Сообщение с заданным ID не найдено'),
		},

	),
)
