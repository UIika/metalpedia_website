# Generated by Django 4.2.3 on 2023-08-12 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0009_alter_profile_user_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='bands.album'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='band',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='bands.band'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='musician',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='bands.musician'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='song',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='bands.song'),
        ),
    ]
