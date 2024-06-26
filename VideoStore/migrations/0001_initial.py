# Generated by Django 5.0.6 on 2024-05-14 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VideoProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('archived', 'Archived')], max_length=10)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
