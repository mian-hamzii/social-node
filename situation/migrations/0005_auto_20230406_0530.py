# Generated by Django 3.2.17 on 2023-04-06 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('situation', '0004_alter_invite_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invite',
            old_name='receiver',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='invite',
            name='sender',
        ),
    ]
