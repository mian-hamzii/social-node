# Generated by Django 4.1.5 on 2023-01-30 09:49

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0007_alter_profile_countries'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='countries',
            field=django_countries.fields.CountryField(default='Choose Country', max_length=2),
        ),
    ]