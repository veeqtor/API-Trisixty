# Generated by Django 2.1.7 on 2019-03-02 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_auto_20190226_1047'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vendor',
            options={'ordering': ('-created_at',)},
        ),
    ]
