from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the currently active user model

class DailyPrize(models.Model):
    day = models.CharField(max_length=100, verbose_name="Challenge day", blank=True, null=True)
    logo = models.ImageField()
    company_name = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    prize_name = models.CharField(max_length=100)
    description = models.TextField()
    video_link = models.URLField()
    thumbnail_video = models.ImageField(blank=True, null=True)
    ig_link = models.URLField(blank=True, null=True)
    tiktok_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    yt_link = models.URLField(blank=True, null=True, verbose_name="Youtube link")
    app_store_link = models.URLField(blank=True, null=True, verbose_name="App store link")
    play_store_link = models.URLField(blank=True, null=True, verbose_name="Play store link")
    class Meta:
        verbose_name = "Daily Prize"
        verbose_name_plural = "Daily Prizes"

    def __str__(self) -> str:
        return self.company_name

class UserPrize(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_prizes')
    prize = models.ForeignKey(DailyPrize, on_delete=models.CASCADE, related_name='prizes_won')
    access_code = models.CharField(max_length=100)
    date_awarded = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Prize"
        verbose_name_plural = "User Prizes"

    def __str__(self) -> str:
        return f"{self.user.username} - {self.prize.prize_name}"
    
class AwardBase(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name

class Medal(AwardBase):
    class Meta:
        verbose_name = "Medal"
        verbose_name_plural = "Medals"

class UserMedal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_medals')
    medal = models.ForeignKey(Medal, on_delete=models.CASCADE, related_name='prizes_won')
    date_awarded = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Medal"
        verbose_name_plural = "User Medals"

    def __str__(self) -> str:
        return f"{self.user.username} - {self.medal.name}"

class Badge(AwardBase):
    class Meta:
        verbose_name = "Badge"
        verbose_name_plural = "Badges"

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='prizes_won')
    date_awarded = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Badge"
        verbose_name_plural = "User Badges"

    def __str__(self) -> str:
        return f"{self.user.username} - {self.badge.name}"

class Trophy(AwardBase):
    class Meta:
        verbose_name = "Trophy"
        verbose_name_plural = "Trophies"

class UserTrophy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_trophies')
    trophy = models.ForeignKey(Trophy, on_delete=models.CASCADE, related_name='prizes_won')
    date_awarded = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Trophy"
        verbose_name_plural = "User Trophies"

    def __str__(self) -> str:
        return f"{self.user.username} - {self.trophy.name}"

