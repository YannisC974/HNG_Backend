from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .models import Event, UserEvent
from django.utils import timezone
from datetime import timedelta
from .serializers import EventSerializer, UserEventSerializer
from rest_framework.response import Response
User = get_user_model()

# class EventSignUpView(generics.RetrieveAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = [IsAuthenticated, ]
#     def get(self, request, *args, **kwargs):
#         event = self.get_object()
#         user = request.user
#         user.events.add(event)
#         user.save()
#         return super().get(request, *args, **kwargs)

# class EventListView(generics.ListAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = [IsAuthenticated, ]

# class EventDetailView(generics.RetrieveAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = [IsAuthenticated, ]
#     lookup_field = "pk"


# Get event by date
class EventsByDateView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = "date"
    def get_queryset(self):
        return Event.objects.filter(date=self.kwargs.get("date"))
    

class FutureEventsView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        gap = self.request.query_params.get('gap', '14')  # Par défaut 2 semaines
        try:
            gap = int(gap)
        except ValueError:
            gap = 14

        today = timezone.now().date()
        end_date = today + timedelta(days=gap)

        return Event.objects.filter(date__gte=today, date__lte=end_date).order_by('date', 'start_time')

class UserEventListView(generics.ListAPIView):
    serializer_class = UserEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserEvent.objects.filter(user=self.request.user)
    
class UserEventCreateView(generics.CreateAPIView):
    serializer_class = UserEventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        event_id = self.request.data.get('event')
        event = Event.objects.get(pk=event_id)
        serializer.save(user=self.request.user, event=event)

class UserEventDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserEvent.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        event_id = request.data.get('event')
        try:
            instance = self.get_queryset().get(event_id=event_id)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserEvent.DoesNotExist:
            return Response({"detail": "User is not registered for this event."}, status=status.HTTP_404_NOT_FOUND)