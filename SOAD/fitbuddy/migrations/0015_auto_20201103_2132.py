# Generated by Django 3.1.3 on 2020-11-03 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitbuddy', '0014_auto_20201103_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
    ]
