# Generated by Django 3.1.2 on 2021-07-26 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0019_auto_20210708_1353'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lon', models.DecimalField(decimal_places=6, max_digits=9)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('article', models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='waypoints', to='mainpage.article')),
            ],
        ),
    ]
