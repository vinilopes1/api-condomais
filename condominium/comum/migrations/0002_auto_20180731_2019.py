# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-07-31 23:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comum', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='unidadehabitacional',
            options={'ordering': ('nome',), 'verbose_name': 'Unidade Habitacional', 'verbose_name_plural': 'Unidades Habitacionais'},
        ),
    ]