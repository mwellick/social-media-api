# Generated by Django 5.0.6 on 2024-06-19 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_rename_following_follow_followed_user_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Unfollow",
        ),
    ]
