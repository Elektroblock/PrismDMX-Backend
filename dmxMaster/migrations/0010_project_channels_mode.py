# Generated by Django 5.0.4 on 2024-05-30 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmxMaster', '0009_remove_fixture_assigned_setup_fader'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='channels_mode',
            field=models.CharField(default='false', max_length=200),
        ),
    ]
