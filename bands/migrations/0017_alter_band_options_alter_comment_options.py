# Generated by Django 4.2.3 on 2023-08-14 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0016_like'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='band',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created']},
        ),
    ]