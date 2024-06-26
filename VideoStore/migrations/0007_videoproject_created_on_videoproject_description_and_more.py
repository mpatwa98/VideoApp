# Generated by Django 5.0.6 on 2024-05-15 17:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VideoStore', '0006_remove_videoproject_thumbnail_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoproject',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videoproject',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='videoproject',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('archived', 'Archived')], default='active', max_length=10),
        ),
        migrations.AddField(
            model_name='videoproject',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='videoproject',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos'),
        ),
    ]
