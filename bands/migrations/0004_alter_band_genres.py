# Generated by Django 4.2.3 on 2023-08-10 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0003_alter_album_cover_alter_band_bandphoto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='band',
            name='genres',
            field=models.CharField(max_length=200),
        ),
    ]
