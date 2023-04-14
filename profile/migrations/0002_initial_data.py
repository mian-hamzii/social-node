from django.db import migrations
from django.core import serializers

from django.core.management import call_command

fixtures = 'initialdata'


def load_fixture(apps, schema_editor):
    call_command('loaddata', fixtures, app_label='profile')


class Migration(migrations.Migration):
    dependencies = [
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture, ),
    ]
