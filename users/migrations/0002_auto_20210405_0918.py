# Generated by Django 3.1.2 on 2021-04-05 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userc',
            name='profile_img',
            field=models.ImageField(default='pm/829952131_3022582.jpg', null=True, upload_to='pm'),
        ),
    ]
