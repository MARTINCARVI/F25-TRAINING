# Generated by Django 4.0.6 on 2022-07-11 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Date'),
        ),
    ]
