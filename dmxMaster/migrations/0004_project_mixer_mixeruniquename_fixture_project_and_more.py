# Generated by Django 5.0.1 on 2024-04-28 13:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmxMaster', '0003_group_mixer_grouplink_mixerpage_mixerfader_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='mixer',
            name='mixerUniqueName',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='fixture',
            name='project',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='dmxMaster.project'),
        ),
        migrations.AddField(
            model_name='group',
            name='project',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='dmxMaster.project'),
        ),
        migrations.AddField(
            model_name='mixer',
            name='project',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='dmxMaster.project'),
        ),
    ]
