# Generated by Django 3.1.2 on 2021-07-09 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210708_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userc',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
