# Generated by Django 4.2.3 on 2023-08-22 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0026_alter_song_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(default='None', max_length=50),
        ),
    ]
