# Generated by Django 5.0.4 on 2024-05-20 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmxMaster', '0006_settings_alter_fixture_fixture_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='setup',
            field=models.CharField(default='false', max_length=200),
        ),
    ]
