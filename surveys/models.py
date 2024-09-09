from django.db import models
from django.contrib.auth import get_user_model
from challenges.models import Challenge
User = get_user_model()

class Survey(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, null=True)
    physical_done = models.BooleanField(default=False)
    mental_done = models.BooleanField(default=False)
    social_done = models.BooleanField(default=False)
    video_link = models.URLField(blank=True, null=True)
    number_of_completed = models.IntegerField(blank=True, null=True)
    class Meta:
        verbose_name = 'Survey'
        verbose_name_plural = 'Surveys'
    def __str__(self) -> str:
        return f'{self.user.email} - {self.challenge.day}'
    
class UserSurvey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    is_choosed = models.BooleanField(default=False)
    is_validated = models.BooleanField(default=False)