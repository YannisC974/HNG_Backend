# Generated by Django 5.0 on 2024-08-13 08:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("challenges", "0002_intensephysicalchallenge_thumbnail_mobile_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="mentalchallenge",
            old_name="image",
            new_name="thumbnail_mobile",
        ),
        migrations.RenameField(
            model_name="socialchallenge",
            old_name="image",
            new_name="thumbnail_mobile",
        ),
        migrations.RemoveField(
            model_name="intensephysicalchallenge",
            name="image",
        ),
        migrations.RemoveField(
            model_name="moderatephysicalchallenge",
            name="image",
        ),
        migrations.AddField(
            model_name="intensephysicalchallenge",
            name="type",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="mentalchallenge",
            name="question",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="mentalchallenge",
            name="thumbnail_square",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
        migrations.AddField(
            model_name="moderatephysicalchallenge",
            name="type",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="socialchallenge",
            name="challenge",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="socialchallenge",
            name="thumbnail_square",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name="challenge",
            name="social",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="challenge_social",
                to="challenges.socialchallenge",
            ),
        ),
        migrations.AlterField(
            model_name="intensephysicalchallenge",
            name="description",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="mentalchallenge",
            name="description",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="moderatephysicalchallenge",
            name="description",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="socialchallenge",
            name="description",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
