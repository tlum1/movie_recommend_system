# Generated by Django 4.1.2 on 2022-10-28 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0011_alter_movie_poster_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='genre',
            new_name='genres',
        ),
    ]