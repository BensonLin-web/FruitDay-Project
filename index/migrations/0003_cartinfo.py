# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-01-24 07:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_auto_20200123_2151'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ccount', models.IntegerField(db_column='ccount')),
                ('goods', models.ForeignKey(db_column='goods_id', on_delete=django.db.models.deletion.CASCADE, to='index.Goods')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='index.User')),
            ],
            options={
                'db_table': 'cart_info',
            },
        ),
    ]