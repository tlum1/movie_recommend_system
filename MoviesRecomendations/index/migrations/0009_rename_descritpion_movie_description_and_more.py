# Generated by Django 4.1.2 on 2022-10-27 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0008_movie_director'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='descritpion',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='movie_ID',
            new_name='movie_id',
        ),
        migrations.AlterField(
            model_name='movie',
            name='poster_link',
            field=models.TextField(verbose_name='Postmter link'),
        ),
    ]