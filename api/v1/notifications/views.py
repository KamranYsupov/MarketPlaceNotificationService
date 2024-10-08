from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings

from .serializers import NotificationSerializer 
from api.v1.utils import send_websocket_data
from api.v1.deps import get_current_user
from notifications.models import Notification


@api_view(['GET']) 
def my_notifications_api_view(request): 
    current_user_data = async_to_sync(get_current_user)(request)
    notifications = Notification.objects.filter(receiver_id=current_user_data['id']) 
    serializer = NotificationSerializer(notifications, many=True)   
       
    return Response( 
        {'data': serializer.data},  
        status=status.HTTP_200_OK, 
    )
   
    
@api_view(['POST'])
def send_notification_api_view(request):
    current_user_data = async_to_sync(get_current_user)(request)
    serializer = NotificationSerializer(data=request.data)
        
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    validated_data = serializer.validated_data
    receiver_id = validated_data['receiver_id']
    async_to_sync(send_websocket_data)(
        uri=f'{settings.WEBSOCKET_BASE_URL}/notifications/{receiver_id}/',
        data=validated_data
    )
                        
    return Response(
        {'message': 'Notification is sent successfully!'},
        status=status.HTTP_201_CREATED
    )
        
    
    
