# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20141115_0647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='performer',
        ),
        migrations.AddField(
            model_name='event',
            name='primaryPerformer',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='secondaryPerformer',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='grouping',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='venue',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
