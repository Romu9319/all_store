# Generated by Django 5.0 on 2024-01-08 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0004_rename_sex_client_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='address',
            field=models.TextField(max_length=50),
        ),
    ]
