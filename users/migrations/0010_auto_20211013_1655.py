# Generated by Django 3.1.2 on 2021-10-13 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20210914_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userc',
            name='profile_img',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
