# Generated by Django 5.0.6 on 2024-06-21 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0010_alter_post_post_media_alter_post_title"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="follow",
            name="is_followed",
        ),
        migrations.RemoveField(
            model_name="like",
            name="is_liked",
        ),
    ]
