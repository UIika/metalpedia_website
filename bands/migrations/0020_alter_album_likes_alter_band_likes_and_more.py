# Generated by Django 4.2.3 on 2023-08-14 15:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bands', '0019_album_likes_band_likes_musician_likes_song_likes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='likes',
            field=models.ManyToManyField(related_name='albums', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='band',
            name='likes',
            field=models.ManyToManyField(related_name='bands', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='musician',
            name='likes',
            field=models.ManyToManyField(related_name='musicians', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='song',
            name='likes',
            field=models.ManyToManyField(related_name='songs', to=settings.AUTH_USER_MODEL),
        ),
    ]
