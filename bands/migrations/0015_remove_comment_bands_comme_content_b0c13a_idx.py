# Generated by Django 4.2.3 on 2023-08-13 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0014_alter_comment_content_type'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='comment',
            name='bands_comme_content_b0c13a_idx',
        ),
    ]
