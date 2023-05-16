# Generated by Django 4.1.5 on 2023-01-23 06:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("enquiry", "0002_enquiry_added_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="enquiry",
            name="added_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="added_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]