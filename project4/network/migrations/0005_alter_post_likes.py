# Generated by Django 3.2.9 on 2021-12-28 15:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20211228_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likedPosts', to=settings.AUTH_USER_MODEL),
        ),
    ]