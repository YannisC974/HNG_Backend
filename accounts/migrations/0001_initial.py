# Generated by Django 5.0 on 2024-08-12 07:48

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("events", "__first__"),
        ("prizes", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="MyUser",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=120, unique=True, verbose_name="E-mail"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
                ("auth_provider", models.CharField(default="email", max_length=255)),
                ("slug", models.SlugField(unique=True)),
                (
                    "activation_token",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("reset_code", models.CharField(blank=True, max_length=50, null=True)),
                ("born_year", models.IntegerField(blank=True, null=True)),
                ("gender", models.CharField(blank=True, max_length=10, null=True)),
                ("is_student", models.BooleanField(default=False)),
                (
                    "university_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("country", models.CharField(blank=True, max_length=100, null=True)),
                ("state", models.CharField(blank=True, max_length=100, null=True)),
                ("city", models.CharField(blank=True, max_length=100, null=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                ("events", models.ManyToManyField(blank=True, to="events.event")),
                ("medals", models.ManyToManyField(blank=True, to="prizes.medal")),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
                "ordering": ["-timestamp"],
            },
        ),
    ]
