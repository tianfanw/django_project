# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('venue', models.CharField(max_length=100)),
                ('performers', models.CharField(max_length=200)),
                ('grouping', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
