# Generated by Django 4.1.2 on 2022-10-26 17:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('index', '0003_movie_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_rating', models.DecimalField(decimal_places=2, max_digits=16, verbose_name='User rating')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Movie', to='index.movie', verbose_name='Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.rating', verbose_name='Ratings')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
