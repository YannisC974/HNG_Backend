# Generated by Django 5.0 on 2024-08-23 07:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("challenges", "0004_remove_intensephysicalchallenge_day_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="challenge",
            name="day",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
