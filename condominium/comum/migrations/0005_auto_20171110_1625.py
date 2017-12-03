# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-10 16:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comum', '0004_auto_20170926_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='condominio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='perfis', to='comum.Condominio'),
        ),
        migrations.AlterField(
            model_name='condominio',
            name='sindico',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='condominio_administrado', to='comum.Perfil'),
        ),
    ]