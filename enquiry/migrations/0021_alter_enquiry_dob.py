# Generated by Django 4.1.7 on 2023-03-31 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquiry', '0020_alter_enquiry_assigned_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquiry',
            name='dob',
            field=models.DateField(blank=True, null=True, verbose_name='Date of Birth'),
        ),
    ]