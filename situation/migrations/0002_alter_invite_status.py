# Generated by Django 3.2.17 on 2023-03-30 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('situation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='status',
            field=models.CharField(choices=[('invite', 'invite'), ('invited', 'invited'), ('accepted', 'accepted'), ('rejected', 'rejected')], default='invite', max_length=50),
        ),
    ]