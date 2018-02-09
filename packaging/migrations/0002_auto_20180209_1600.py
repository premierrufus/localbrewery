# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-09 16:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packaging', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packagingevent',
            name='packager',
            field=models.CharField(blank=True, choices=[('tyler', 'Tyler'), ('ron', 'Ron'), ('chris', 'Chris'), ('shea', 'Shea'), ('ian', 'Ian'), ('brandon', 'Brandon')], max_length=100, null=True, verbose_name='name of packager'),
        ),
    ]
