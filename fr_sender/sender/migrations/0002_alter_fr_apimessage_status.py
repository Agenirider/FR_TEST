# Generated by Django 3.2.8 on 2022-12-15 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sender', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fr_apimessage',
            name='status',
            field=models.CharField(choices=[('created', 'created'), ('in_progress', 'in_progress'), ('done', 'done'), ('failed', 'failed')], default='created', max_length=30),
        ),
    ]