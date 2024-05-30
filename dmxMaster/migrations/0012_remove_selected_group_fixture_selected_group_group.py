# Generated by Django 5.0.4 on 2024-05-30 09:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmxMaster', '0011_selected_fixture_selected_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selected_group',
            name='fixture',
        ),
        migrations.AddField(
            model_name='selected_group',
            name='group',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='dmxMaster.group'),
        ),
    ]
