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
                ('title', models.CharField(max_length=200, null=True)),
                ('venue', models.CharField(max_length=100, null=True)),
                ('primaryPerformer', models.CharField(max_length=200, null=True)),
                ('secondaryPerformer', models.CharField(max_length=200, null=True)),
                ('grouping', models.CharField(max_length=100, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('quantity', models.IntegerField()),
                ('zoneId', models.IntegerField(null=True)),
                ('zoneName', models.CharField(max_length=200, null=True)),
                ('sectionId', models.IntegerField(null=True)),
                ('sectionName', models.CharField(max_length=200, null=True)),
                ('row', models.CharField(max_length=200)),
                ('seatNumbers', models.CharField(max_length=200)),
                ('currentPrice', models.FloatField(null=True)),
                ('event', models.ForeignKey(to='myapp.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SoldTicket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('listingId', models.IntegerField()),
                ('zoneId', models.IntegerField(null=True)),
                ('zoneName', models.CharField(max_length=200, null=True)),
                ('sectionId', models.IntegerField(null=True)),
                ('sectionName', models.CharField(max_length=200, null=True)),
                ('row', models.CharField(max_length=200)),
                ('seatNumber', models.CharField(max_length=200, null=True)),
                ('currentPrice', models.FloatField(null=True)),
                ('event', models.ForeignKey(to='myapp.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
