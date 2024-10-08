from rest_framework import serializers

from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    receiver_id = serializers.CharField(
        max_length=100,
        write_only=False
    )
    
    class Meta:
        model = Notification
        fields = ('text', 'event_link', 'receiver_id')

class NotificationsListSerializer(serializers.Serializer):
    notifications = serializers.ListField()
    