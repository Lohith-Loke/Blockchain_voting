# Generated by Django 4.2.6 on 2023-10-31 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_election_isused'),
    ]

    operations = [
        migrations.AddField(
            model_name='adharcard',
            name='rand',
            field=models.CharField(auto_created=True, default='dZlm9Lsu13h69XiUORmi', max_length=50),
        ),
    ]