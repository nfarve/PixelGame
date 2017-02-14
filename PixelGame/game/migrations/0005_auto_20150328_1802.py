# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20150328_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='letters',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='time_till_flip',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lastPlayed',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 28, 18, 2, 49, 863337)),
            preserve_default=True,
        ),
    ]
