# Generated by Django 5.0.2 on 2024-07-12 16:06

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("personal_assistant_backend", "0003_delete_test"),
    ]

    operations = [
        migrations.CreateModel(
            name="Chat",
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
                ("email", models.TextField()),
                (
                    "guid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("user_input", models.TextField()),
                ("ai_response", models.TextField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
