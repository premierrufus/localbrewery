# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-09 16:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('packaging', '0002_auto_20180209_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packagingevent',
            name='brewing_event',
            field=models.ForeignKey(blank=True, help_text='BrewingEvent associated with this packaging event.', null=True, on_delete=django.db.models.deletion.CASCADE, to='brewing.BrewingEvent', verbose_name='Source'),
        ),
        migrations.AlterField(
            model_name='packagingevent',
            name='packaging_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='Date'),
        ),
    ]
