# Generated by Django 3.1.4 on 2020-12-26 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smsapp', '0002_auto_20201127_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavereportstaff',
            name='leave_status',
            field=models.IntegerField(default=0),
        ),
    ]
