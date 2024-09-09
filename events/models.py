from django.db import models
from challenges.models import Instructor
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the currently active user model

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    link = models.URLField(verbose_name="Link to the event")
    type_of_event = models.CharField(max_length=100, verbose_name="Event name")
    requirements = models.CharField(max_length=100)
    instructor = models.ManyToManyField(Instructor, blank=True)
    thumbnail = models.ImageField(blank=True, null=True)
    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
    def __str__(self) -> str:
        return self.day
    
class UserEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_event')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_subscribed')

    class Meta:
        verbose_name = "User Event"
        verbose_name_plural = "User Events"

    def __str__(self) -> str:
        return f"{self.user.username} - {self.event.title}"
