# Generated by Django 5.1.1 on 2024-09-24 13:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_alter_studentmodel_guardian_name_and_more'),
        ('transaction', '0002_alter_transactionmodel_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionmodel',
            name='hostel_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='student.studentmodel'),
        ),
    ]
