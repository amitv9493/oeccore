# Generated by Django 4.1.5 on 2023-01-23 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("enquiry", "0004_alter_enquiry_country_interested_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="university",
            name="univ_logo",
            field=models.ImageField(upload_to="universitylogo"),
        ),
    ]
