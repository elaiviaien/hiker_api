# Generated by Django 3.1.2 on 2021-04-22 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('city_country', '0001_initial'),
        ('mainpage', '0013_article_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='country',
            field=models.ManyToManyField(blank=True, related_name='countries', to='city_country.Country'),
        ),
        migrations.RemoveField(
            model_name='article',
            name='city',
        ),
        migrations.AddField(
            model_name='article',
            name='city',
            field=models.ManyToManyField(blank=True, related_name='cities', to='city_country.City'),
        ),
    ]
