# Generated by Django 2.1.2 on 2020-06-13 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_auto_20200613_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='e_table',
            name='kscj',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='e_table',
            name='pscj',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='e_table',
            name='zpcj',
            field=models.CharField(max_length=10, null=True),
        ),
    ]