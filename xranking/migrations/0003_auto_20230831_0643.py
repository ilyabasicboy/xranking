# Generated by Django 2.2.28 on 2023-08-31 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xranking', '0002_auto_20230728_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='search_engine',
            field=models.CharField(default='google', max_length=255),
        ),
    ]