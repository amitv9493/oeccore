# Generated by Django 4.1.7 on 2023-03-15 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquiry', '0010_phonenumbers'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='date_created',
            field=models.DateField(blank=True, null=True),
        ),
    ]