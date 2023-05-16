# Generated by Django 4.1.5 on 2023-01-20 07:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("master", "0001_initial"),
        ("enquiry", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Application",
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
                ("Tenth_Marksheet", models.ImageField(null=True, upload_to="media")),
                ("Twelveth_Marksheet", models.ImageField(null=True, upload_to="media")),
                ("Diploma_Marksheet", models.ImageField(null=True, upload_to="media")),
                ("Bachelor_Marksheet", models.ImageField(null=True, upload_to="media")),
                ("Master_Marksheet", models.ImageField(null=True, upload_to="media")),
                ("Lor", models.ImageField(null=True, upload_to="media")),
                ("Sop", models.ImageField(null=True, upload_to="media")),
                ("Resume", models.ImageField(null=True, upload_to="media")),
                ("Language_Exam", models.ImageField(null=True, upload_to="media")),
                (
                    "assigned_users",
                    models.ForeignKey(
                        default="",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="enquiry.enquiry",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="master.application_status",
                    ),
                ),
            ],
        ),
    ]