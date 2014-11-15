# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20141115_0645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soldticket',
            name='sectionId',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='soldticket',
            name='sectionName',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='sectionId',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='sectionName',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
    ]
