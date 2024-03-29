# Generated by Django 5.0.1 on 2024-02-06 11:36

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0002_alter_post_options"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="like_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="postattachments",
            name="image",
            field=models.ImageField(blank=True, upload_to="post_attachments"),
        ),
        migrations.CreateModel(
            name="Like",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="like",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="post",
            name="like",
            field=models.ManyToManyField(blank=True, to="post.like"),
        ),
    ]
