# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='lastPlayed',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 28, 18, 1, 40, 764566)),
            preserve_default=True,
        ),
    ]
