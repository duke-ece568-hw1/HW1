# Generated by Django 2.1.5 on 2019-01-28 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20190127_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='isSharable',
            field=models.BooleanField(default=True),
        ),
    ]
