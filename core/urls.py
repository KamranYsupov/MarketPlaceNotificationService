from django.contrib import admin
from django.urls import path, include

from notifications.consumers import NotificationConsumer


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.v1.urls', namespace='api_v1'))
]

websocket_urlpatterns = [
    path('notifications/<receiver_id>/', NotificationConsumer.as_asgi()),
]
