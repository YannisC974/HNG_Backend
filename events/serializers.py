from rest_framework import serializers
from .models import Event, Event, UserEvent
from django.contrib.auth import get_user_model
from challenges.serializers import InstructorSerializer

User = get_user_model()

class EventSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'day', 'title', 'description', 'start_time', 'end_time', 
                  'date', 'link', 'type_of_event', 'requirements', 'instructor', 
                  'thumbnail']

class UserEventSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(),
        source='event',
        write_only=True
    )

    class Meta:
        model = UserEvent
        fields = ['id', 'user', 'event', 'event_id']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        event = validated_data['event']
        return UserEvent.objects.create(user=user, event=event)