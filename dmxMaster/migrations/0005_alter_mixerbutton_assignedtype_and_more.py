# Generated by Django 5.0.1 on 2024-04-28 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmxMaster', '0004_project_mixer_mixeruniquename_fixture_project_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mixerbutton',
            name='assignedType',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='mixerfader',
            name='assignedType',
            field=models.CharField(max_length=200),
        ),
    ]