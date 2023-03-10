# Generated by Django 3.2.8 on 2022-12-15 04:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DistributionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='DistributionStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FR_APIClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(regex=re.compile('^7*(?P<def_code>\\d{3})(?P<phone_number>\\d{7})$'))])),
                ('def_plmn_code', models.CharField(blank=True, max_length=3, null=True)),
                ('tag', models.CharField(blank=True, max_length=30, null=True)),
                ('time_zone', models.CharField(default='UTC', max_length=5)),
            ],
            options={
                'verbose_name_plural': 'Clients',
                'db_table': 'clients',
            },
        ),
        migrations.CreateModel(
            name='FR_APIDistributionTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_task', models.DateTimeField()),
                ('modified_task', models.DateTimeField(null=True)),
                ('start_task', models.DateTimeField(blank=True, null=True)),
                ('end_task', models.DateTimeField(blank=True, null=True)),
                ('message', models.CharField(max_length=300)),
                ('def_plmn_code', models.CharField(blank=True, max_length=3, null=True)),
                ('tag', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'verbose_name_plural': 'Distribution Tasks',
                'db_table': 'distribution_task',
            },
        ),
        migrations.CreateModel(
            name='FR_APIMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('created', 'created'), ('in_progress', 'in_progress'), ('finished', 'finished')], default='created', max_length=30)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sender.fr_apiclient')),
                ('distribution_task', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='task', to='sender.fr_apidistributiontask')),
            ],
            options={
                'verbose_name_plural': 'Messages',
                'db_table': 'message',
            },
        ),
    ]
