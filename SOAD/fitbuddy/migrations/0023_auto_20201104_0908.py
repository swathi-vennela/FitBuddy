# Generated by Django 3.1.3 on 2020-11-04 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitbuddy', '0022_auto_20201104_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitnesscenter',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
