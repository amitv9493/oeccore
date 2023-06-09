# Generated by Django 4.1.5 on 2023-01-21 02:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("master", "0001_initial"),
        ("application", "0003_remove_application_bachelor_marksheet_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="application",
            name="Bachelor_Marksheet",
            field=models.ImageField(null=True, upload_to="media"),
        ),
        migrations.AddField(
            model_name="application",
            name="Diploma_Marksheet",
            field=models.ImageField(null=True, upload_to="media"),
        ),
        migrations.AddField(
            model_name="application",
            name="Language_Exam",
            field=models.ImageField(null=True, upload_to="media"),
        ),
        migrations.AddField(
            model_name="application",
            name="Lor",
            field=models.ImageField(null=True, upload_to="media"),
        ),
        migrations.AddField(
            model_name="application",
            name="Master_Marksheet",
            field=models.ImageField(null=True, upload_to="media"),
        ),
        migrations.AddField(
            model_name="application",
            name="Resume",
            field=models.ImageField(null=True, upload_to="media"),
        ),
        migrations.AddField(
            model_name="application",
            name="Sop",
            field=models.ImageField(null=True, upload_to="media"),
        ),
        migrations.AddField(
            model_name="application",
            name="Twelveth_Marksheet",
            field=models.ImageField(null=True, upload_to="media"),
        ),
        migrations.AddField(
            model_name="application",
            name="assigned_users",
            field=models.ForeignKey(
                default="",
                limit_choices_to={"is_active": True},
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="application",
            name="status",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="master.application_status",
            ),
            preserve_default=False,
        ),
    ]
