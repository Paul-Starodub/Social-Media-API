# Generated by Django 4.2.1 on 2023-05-20 06:16

from django.db import migrations, models
import post.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Commentary",
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
                ("commentary", models.CharField(max_length=350)),
            ],
        ),
        migrations.CreateModel(
            name="Like",
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
                ("object_id", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Post",
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
                ("create_date", models.DateField(auto_now=True)),
                ("content", models.CharField(max_length=280)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=post.models.movie_image_file_path,
                    ),
                ),
            ],
            options={
                "ordering": ["-create_date"],
            },
        ),
    ]