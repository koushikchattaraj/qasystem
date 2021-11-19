# Generated by Django 3.2.7 on 2021-09-29 14:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0010_auto_20210929_0903'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='created_at',
            field=models.TimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='folder',
            name='created_at',
            field=models.TimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]