# Generated by Django 4.1.2 on 2022-10-25 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.TextField(default='', verbose_name='Genre'),
            preserve_default=False,
        ),
    ]
