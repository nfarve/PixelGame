# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20150328_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='lastPlayed',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 28, 18, 2, 18, 156942)),
            preserve_default=True,
        ),
    ]
