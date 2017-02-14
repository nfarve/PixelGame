# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import game.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('croppedImage', models.ImageField(upload_to=game.models.changeName)),
                ('position_x', models.IntegerField()),
                ('position_y', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CropOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField()),
                ('order', models.CommaSeparatedIntegerField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wholeImage', models.ImageField(upload_to=b'wholeImages/')),
                ('level', models.IntegerField(default=1)),
                ('answer', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0)),
                ('lastPlayed', models.DateTimeField(default=datetime.datetime(2015, 3, 28, 18, 1, 21, 641677))),
                ('flips', models.IntegerField(default=3)),
                ('level', models.IntegerField(default=1)),
                ('cropNumber', models.IntegerField(default=5)),
                ('hints', models.IntegerField(default=0)),
                ('letters', models.CharField(default=b'', max_length=10000)),
                ('time_till_flip', models.IntegerField(default=120)),
                ('bestTime', models.CharField(default=b'', max_length=20000000)),
                ('achievements', models.CharField(default=b'', max_length=2000000)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='crop',
            name='image',
            field=models.ForeignKey(to='game.Image'),
            preserve_default=True,
        ),
    ]
