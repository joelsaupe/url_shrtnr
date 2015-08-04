# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('actual_url', models.CharField(max_length=2083)),
                ('shortend_url', models.CharField(max_length=2083)),
                ('views', models.IntegerField(default=0)),
            ],
        ),
    ]
