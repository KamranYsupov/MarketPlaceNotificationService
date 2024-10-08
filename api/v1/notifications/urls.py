from django.urls import path

from . import views


urlpatterns = [
    path(
        'mine/',
        views.my_notifications_api_view,
        name='my_notifications',
    ),
    path(
        'send/',
        views.send_notification_api_view, 
        name='send_notification'
    ),
]