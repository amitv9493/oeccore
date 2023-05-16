# Generated by Django 4.1.7 on 2023-02-16 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0004_alter_application_status_options_and_more'),
        ('enquiry', '0007_delete_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='intake',
        ),
        migrations.AddField(
            model_name='course',
            name='intake',
            field=models.ManyToManyField(to='master.intake'),
        ),
    ]