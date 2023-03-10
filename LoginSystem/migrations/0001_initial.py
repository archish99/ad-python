# Generated by Django 4.1 on 2022-08-26 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BLUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255, unique=True)),
                ('FirstName', models.CharField(max_length=100)),
                ('LastName', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=200)),
                ('PublicAdress', models.CharField(max_length=255)),
                ('config', models.TextField(verbose_name='')),
                ('logintype', models.IntegerField(verbose_name=6)),
            ],
        ),
        migrations.CreateModel(
            name='RestAPIKeys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('APISecret', models.CharField(max_length=255, unique=True)),
            ],
        ),
    ]
