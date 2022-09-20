# Generated by Django 4.1 on 2022-09-18 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('productId', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('productName', models.CharField(max_length=100)),
                ('productDesc', models.TextField()),
                ('price', models.IntegerField()),
            ],
        ),
    ]