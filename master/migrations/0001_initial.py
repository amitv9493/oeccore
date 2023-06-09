# Generated by Django 4.1.5 on 2023-01-20 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="application_status",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("App_status", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="course_levels",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("levels", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="course_requirements",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("requirement", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name_plural": "Course requirements",
            },
        ),
        migrations.CreateModel(
            name="current_education",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("current_education", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name_plural": "Current Education",
            },
        ),
        migrations.CreateModel(
            name="documents_required",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("docu_name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="enquiry_status",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="intake",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("intake_month", models.CharField(max_length=10)),
                ("intake_year", models.IntegerField()),
            ],
        ),
    ]
