# Generated by Django 5.1.1 on 2024-10-03 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_alter_studentmodel_guardian_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentmodel',
            name='guardian_mobile',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='studentmodel',
            name='parent_mobile',
            field=models.BigIntegerField(),
        ),
    ]
