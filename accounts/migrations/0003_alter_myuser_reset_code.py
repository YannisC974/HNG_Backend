# Generated by Django 5.0 on 2024-08-22 09:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_remove_myuser_events_remove_myuser_medals_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="myuser",
            name="reset_code",
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
