from django.db import models

LEVEL_CHOICE = (
    ("moderate", "moderate"),
    ("intense", "intense"),
)

class Challenge(models.Model):
    day = models.CharField(max_length=100, verbose_name="Challenge day", blank=True, null=True)
    quote = models.TextField(blank=True, null=True)
    author_name = models.CharField(max_length=100, blank=True, null=True)
    video_link = models.URLField(max_length=250, blank=True, null=True)
    thumbnail_video = models.ImageField(blank=True, null=True)
    moderate_physical = models.ForeignKey("ModeratePhysicalChallenge", on_delete=models.SET_NULL, blank=True, null=True)
    intense_physical = models.ForeignKey("IntensePhysicalChallenge", on_delete=models.SET_NULL, blank=True, null=True)
    mental = models.ForeignKey("MentalChallenge", on_delete=models.SET_NULL, blank=True, null=True)
    social = models.ForeignKey("SocialChallenge", related_name='challenge_social', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'Challenge'
        verbose_name_plural = 'Challenges'

    def __str__(self) -> str:
        return self.day


class CommonChallengeFields(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    banner_desktop = models.ImageField(blank=True, null=True)
    banner_mobile = models.ImageField(blank=True, null=True)
    thumbnail_square = models.ImageField(blank=True, null=True)
    thumbnail_mobile = models.ImageField(blank=True, null=True)

    class Meta:
        abstract = True


class AbstractPhysicalChallenge(CommonChallengeFields):
    workout_name = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    required_equipments = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    instructor = models.ForeignKey("Instructor", on_delete=models.SET_NULL, blank=True, null=True)
    video = models.URLField(max_length=250, blank=True, null=True)
    thumbnail_video = models.ImageField(blank=True, null=True)

    class Meta:
        abstract = True


class ModeratePhysicalChallenge(AbstractPhysicalChallenge):
    class Meta:
        verbose_name = 'Moderate Physical Challenge'
        verbose_name_plural = 'Moderate Physical Challenges'


class IntensePhysicalChallenge(AbstractPhysicalChallenge):
    class Meta:
        verbose_name = 'Intense Physical Challenge'
        verbose_name_plural = 'Intense Physical Challenges'


class SocialChallenge(CommonChallengeFields):
    challenge = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        verbose_name = 'Social Challenge'
        verbose_name_plural = 'Social Challenges'


class MentalChallenge(CommonChallengeFields):
    question = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    voice_recording = models.FileField(blank=True, null=True)
    class Meta:
        verbose_name = 'Mental Challenge'
        verbose_name_plural = 'Mental Challenges'


class Instructor(models.Model):
    image = models.ImageField(blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name="Instructor name")
    description = models.TextField()
    ig_link = models.URLField(blank=True, null=True)
    tiktok_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    yt_link = models.URLField(blank=True, null=True, verbose_name="Youtube link")

    class Meta:
        verbose_name = 'Instructor'
        verbose_name_plural = 'Instructors'

    def __str__(self) -> str:
        return self.name
