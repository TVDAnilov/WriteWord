# Generated by Django 4.1.3 on 2022-11-09 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_interruptcheckwordknow_userid_worldowner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='words',
            name='UserID_WorldOwner',
        ),
    ]
