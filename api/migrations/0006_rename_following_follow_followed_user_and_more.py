# Generated by Django 5.0.6 on 2024-06-18 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_rename_post_comment_comment_post"),
    ]

    operations = [
        migrations.RenameField(
            model_name="follow",
            old_name="following",
            new_name="followed_user",
        ),
        migrations.RenameField(
            model_name="unfollow",
            old_name="unfollowed",
            new_name="unfollowed_user",
        ),
    ]
