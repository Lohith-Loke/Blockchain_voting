# Generated by Django 4.2.6 on 2023-10-31 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_alter_election_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='Duration',
            field=models.DurationField(blank=True, null=True),
        ),
    ]