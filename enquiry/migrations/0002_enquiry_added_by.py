# Generated by Django 4.1.5 on 2023-01-21 04:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("enquiry", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="enquiry",
            name="added_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="added_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
