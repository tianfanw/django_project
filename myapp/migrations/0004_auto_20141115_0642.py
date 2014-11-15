# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_ticket'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoldTicket',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('quantity', models.IntegerField()),
                ('zoneId', models.IntegerField()),
                ('zoneName', models.CharField(max_length=200)),
                ('sectionId', models.IntegerField()),
                ('sectionName', models.CharField(max_length=200)),
                ('row', models.CharField(max_length=200)),
                ('seatNumbers', models.CharField(max_length=200)),
                ('currentPrice', models.FloatField()),
                ('event', models.ForeignKey(to='myapp.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='ticket',
            old_name='eventId',
            new_name='event',
        ),
    ]
