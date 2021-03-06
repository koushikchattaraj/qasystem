# Generated by Django 3.2.7 on 2021-09-22 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0007_alter_folder_parents'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='folder',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='folder',
            name='parents',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='folder', to='drive.folder'),
        ),
    ]
