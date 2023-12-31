# Generated by Django 4.2.6 on 2023-11-03 01:27

from django.db import migrations, models
import polls.models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_adharcard_rand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adharcard',
            name='adharnumber',
            field=models.CharField(max_length=12, primary_key=True, serialize=False, unique=True, validators=[polls.models.CustomValidators.adharvalidator]),
        ),
        migrations.AlterField(
            model_name='adharcard',
            name='rand',
            field=models.CharField(auto_created=True, default='1AW36HcsynwYGaHa3Iuh', editable=False, max_length=50),
        ),
    ]
