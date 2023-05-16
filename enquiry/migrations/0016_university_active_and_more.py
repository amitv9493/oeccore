# Generated by Django 4.1.7 on 2023-03-23 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enquiry', '0015_alter_enquiry_assigned_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='university_interested',
            field=models.ForeignKey(blank=True, limit_choices_to={'active': True, 'university__active': True}, null=True, on_delete=django.db.models.deletion.CASCADE, to='enquiry.university'),
        ),
    ]