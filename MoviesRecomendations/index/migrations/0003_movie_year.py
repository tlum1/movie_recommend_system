# Generated by Django 4.1.2 on 2022-10-26 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_movie_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='year',
            field=models.PositiveIntegerField(default=0, verbose_name='Year'),
            preserve_default=False,
        ),
    ]
