# Generated by Django 4.1.7 on 2023-02-21 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquiry', '0008_remove_course_intake_course_intake'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]