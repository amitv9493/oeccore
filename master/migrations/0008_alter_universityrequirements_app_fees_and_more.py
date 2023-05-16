# Generated by Django 4.1.7 on 2023-03-30 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0007_universityrequirements_course_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='universityrequirements',
            name='app_fees',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Application Fees'),
        ),
        migrations.AlterField(
            model_name='universityrequirements',
            name='change_of_agent',
            field=models.CharField(choices=[('YES', 'Yes'), ('NO', 'No'), ('University Discretion', 'University Discreation')], max_length=50, verbose_name='Change of agent'),
        ),
    ]
