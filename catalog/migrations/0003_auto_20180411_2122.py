# Generated by Django 2.0 on 2018-04-11 21:22

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20180411_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='effect',
            name='authors',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), blank=True, size=None),
        ),
        migrations.AlterField(
            model_name='effect',
            name='maintainers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), blank=True, size=None),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('name', 'parent')},
        ),
    ]