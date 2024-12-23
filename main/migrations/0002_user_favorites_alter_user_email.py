# Generated by Django 5.1.4 on 2024-12-23 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorited_by', to='main.boardgame'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=60, unique=True, verbose_name='Електронна адреса'),
        ),
    ]
