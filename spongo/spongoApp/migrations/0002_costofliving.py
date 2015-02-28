# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spongoApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostOfLiving',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country_name', models.DecimalField(max_digits=8, decimal_places=2)),
                ('accommodation', models.DecimalField(max_digits=8, decimal_places=2)),
                ('food', models.DecimalField(max_digits=8, decimal_places=2)),
                ('water', models.DecimalField(max_digits=8, decimal_places=2)),
                ('local_transportation', models.DecimalField(max_digits=8, decimal_places=2)),
                ('entertainment', models.DecimalField(max_digits=8, decimal_places=2)),
                ('communication', models.DecimalField(max_digits=8, decimal_places=2)),
                ('tips', models.DecimalField(max_digits=8, decimal_places=2)),
                ('intercity_trasport', models.DecimalField(max_digits=8, decimal_places=2)),
                ('souvenirs', models.DecimalField(max_digits=8, decimal_places=2)),
                ('scams_robberies_mishaps', models.DecimalField(max_digits=8, decimal_places=2)),
                ('alcohol', models.DecimalField(max_digits=8, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
