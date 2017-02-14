# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_auto_20150328_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='letters',
            field=models.CharField(default=b'', max_length=10000),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='time_till_flip',
            field=models.IntegerField(default=120),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lastPlayed',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 28, 18, 3, 3, 262506)),
            preserve_default=True,
        ),
    ]
