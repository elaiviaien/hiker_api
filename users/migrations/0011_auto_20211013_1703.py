# Generated by Django 3.1.2 on 2021-10-13 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20211013_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userc',
            name='profile_img',
            field=models.ImageField(default='C:\\Users\\o_1ivka\\Documents\\Myweb\\server\\hiker\\media\\test.jpg', null=True, upload_to=''),
        ),
    ]
