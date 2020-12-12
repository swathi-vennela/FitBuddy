# Generated by Django 3.1.4 on 2020-12-12 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FitnessEquipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('type', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
            ],
        ),
    ]
