# Generated by Django 4.1.7 on 2023-03-14 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0009_remove_application_bachelor_marksheet_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='Tenth_Marksheet',
            field=models.ImageField(blank=True, null=True, upload_to='media/images'),
        ),
    ]
