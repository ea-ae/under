# Generated by Django 2.1 on 2018-08-20 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0023_auto_20180820_1844'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cult',
            name='recruitment_target',
        ),
    ]
