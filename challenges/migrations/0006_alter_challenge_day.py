# Generated by Django 5.0 on 2024-08-23 07:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("challenges", "0005_alter_challenge_day"),
    ]

    operations = [
        migrations.AlterField(
            model_name="challenge",
            name="day",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Challenge day"
            ),
        ),
    ]
