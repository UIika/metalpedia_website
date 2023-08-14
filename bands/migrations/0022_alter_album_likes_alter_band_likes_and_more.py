# Generated by Django 4.2.3 on 2023-08-14 15:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bands', '0021_alter_album_likes_alter_band_likes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='albums', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='band',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='bands', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='musician',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='musicians', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='song',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='songs', to=settings.AUTH_USER_MODEL),
        ),
    ]
