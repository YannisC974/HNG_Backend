# Generated by Django 5.0 on 2024-08-12 07:50

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("challenges", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("day", models.CharField(max_length=100, verbose_name="Challenge day")),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                ("date", models.DateField()),
                ("link", models.URLField(verbose_name="Link to the event")),
                ("name", models.CharField(max_length=100, verbose_name="Event name")),
                ("requirements", models.CharField(max_length=100)),
                ("image", models.URLField(verbose_name="Link to the image")),
                (
                    "instructor",
                    models.ManyToManyField(blank=True, to="challenges.instructor"),
                ),
            ],
            options={
                "verbose_name": "Event",
                "verbose_name_plural": "Events",
            },
        ),
    ]
