# Generated by Django 2.1.7 on 2019-02-25 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0002_auto_20190221_1231'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True)),
                ('deleted', models.BooleanField(default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=200)),
                ('updated_by', models.CharField(blank=True, max_length=200)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='business Name')),
                ('location', models.CharField(max_length=255, verbose_name='business Location')),
                ('description', models.TextField(blank=True, verbose_name='business description')),
                ('logo_url', models.CharField(max_length=255, verbose_name='logo URI')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='email')),
                ('phone', models.CharField(max_length=20, verbose_name='phone')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'db_table': 'vendors',
            },
        ),
    ]
