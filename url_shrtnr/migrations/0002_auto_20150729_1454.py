# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('url_shrtnr', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='url',
            old_name='shortend_url',
            new_name='slug',
        ),
        migrations.RenameField(
            model_name='url',
            old_name='actual_url',
            new_name='url',
        ),
    ]
