# Generated by Django 2.1 on 2018-08-11 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20180811_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cult',
            name='headquarters',
            field=models.TextField(default='[]'),
        ),
    ]
