# Generated by Django 2.1.5 on 2019-01-26 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20190126_2245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='name',
        ),
    ]