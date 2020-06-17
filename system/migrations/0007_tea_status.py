# Generated by Django 2.1.2 on 2020-06-17 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_auto_20200617_1118'),
    ]

    operations = [
        migrations.CreateModel(
            name='tea_status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xm', models.CharField(max_length=20)),
                ('bsrq', models.DateField(max_length=12)),
                ('zk', models.CharField(max_length=10)),
                ('tw', models.CharField(max_length=5)),
                ('gh', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.teacher')),
                ('yxh', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.department')),
            ],
        ),
    ]
