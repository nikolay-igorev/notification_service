from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('clients', views.ClientViewSet, basename='client')
router.register('notifications', views.NotificationViewSet, basename='notification')
router.register('messages', views.MessageViewSet, basename='message')

urlpatterns = router.urls
