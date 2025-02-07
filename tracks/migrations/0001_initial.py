# Generated by Django 5.0.3 on 2024-03-17 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('artists', models.CharField(max_length=100)),
                ('album', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=300)),
                ('img_url', models.CharField(max_length=300)),
            ],
        ),
    ]
