# Generated by Django 3.1.14 on 2023-01-16 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LoginSystem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bluser',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='restapikeys',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]