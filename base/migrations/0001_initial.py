# Generated by Django 3.2.7 on 2021-09-22 10:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="AccessUrl",
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
                ("name", models.CharField(default=" ", max_length=50)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("expires_in", models.DurationField(blank=True, null=True)),
                ("object_id", models.PositiveIntegerField()),
                ("url", models.URLField()),
                (
                    "url_type",
                    models.CharField(
                        choices=[
                            ("SHORT", "SHORTENED URL"),
                            ("FRONTEND", "FRONTEND URL"),
                            ("MEDIA", "MEDIA URL"),
                            ("STREAM", "STREAM URL"),
                        ],
                        max_length=10,
                    ),
                ),
                ("description", models.TextField(default="")),
                ("active", models.BooleanField(default=False)),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "unique_together": {("content_type", "object_id", "url_type")},
            },
        ),
    ]
