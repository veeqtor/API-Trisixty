# Generated by Django 2.1.7 on 2019-03-02 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20190302_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.Vendor'),
        ),
    ]
