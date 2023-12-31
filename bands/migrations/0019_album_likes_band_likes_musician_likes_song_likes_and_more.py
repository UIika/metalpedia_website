# Generated by Django 4.2.3 on 2023-08-14 15:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bands', '0018_alter_like_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='likes',
            field=models.ManyToManyField(related_query_name='albums', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='band',
            name='likes',
            field=models.ManyToManyField(related_query_name='bands', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='musician',
            name='likes',
            field=models.ManyToManyField(related_query_name='musicians', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='song',
            name='likes',
            field=models.ManyToManyField(related_query_name='songs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
