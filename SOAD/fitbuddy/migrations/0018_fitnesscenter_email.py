# Generated by Django 3.1.3 on 2020-11-04 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitbuddy', '0017_auto_20201103_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='fitnesscenter',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
    ]
