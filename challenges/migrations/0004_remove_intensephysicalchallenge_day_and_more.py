# Generated by Django 5.0 on 2024-08-14 08:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("challenges", "0003_rename_image_mentalchallenge_thumbnail_mobile_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="intensephysicalchallenge",
            name="day",
        ),
        migrations.RemoveField(
            model_name="mentalchallenge",
            name="day",
        ),
        migrations.RemoveField(
            model_name="moderatephysicalchallenge",
            name="day",
        ),
        migrations.RemoveField(
            model_name="socialchallenge",
            name="day",
        ),
    ]
