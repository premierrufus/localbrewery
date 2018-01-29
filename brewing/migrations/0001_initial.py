# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-29 21:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Beer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Trade Name')),
            ],
        ),
        migrations.CreateModel(
            name='BrewingEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brew_date', models.DateField(default=django.utils.timezone.now)),
                ('brewed_beer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brewing.Beer')),
            ],
            options={
                'verbose_name': 'Brewing Event',
            },
        ),
        migrations.CreateModel(
            name='Gyle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_number', models.CharField(max_length=7, verbose_name='#')),
            ],
        ),
        migrations.AddField(
            model_name='brewingevent',
            name='gyle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brewing.Gyle'),
        ),
        migrations.AddField(
            model_name='brewingevent',
            name='gyle2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='brewing.Gyle'),
        ),
        migrations.AddField(
            model_name='brewingevent',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
