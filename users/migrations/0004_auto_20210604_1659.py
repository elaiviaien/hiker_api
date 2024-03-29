# Generated by Django 3.1.2 on 2021-06-04 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userc_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('background_img', models.ImageField(null=True, upload_to='pm')),
                ('logo_outline', models.ImageField(null=True, upload_to='pm')),
            ],
        ),
        migrations.AddField(
            model_name='userc',
            name='region',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_region', to='users.region', verbose_name='регион'),
        ),
    ]
