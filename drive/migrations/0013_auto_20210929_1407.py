# Generated by Django 3.2.7 on 2021-09-29 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0012_auto_20210929_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='created_at',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='folder',
            name='created_at',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
