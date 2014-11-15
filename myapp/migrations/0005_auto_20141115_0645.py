# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20141115_0642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soldticket',
            name='zoneId',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='soldticket',
            name='zoneName',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='zoneId',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='zoneName',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
    ]
