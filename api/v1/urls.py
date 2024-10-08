from django.urls import path, include

app_name = 'api_v1'

urlpatterns = [
    path('notifications/', include('api.v1.notifications.urls')),
]