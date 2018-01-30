# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-30 21:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=50, verbose_name='Contact Name')),
                ('name', models.CharField(max_length=50, verbose_name='Account Name')),
                ('notes', models.TextField()),
                ('status', models.CharField(blank=True, choices=[('a', 'Active'), ('i', 'Inactive')], default='a', max_length=1, verbose_name='Account Status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
