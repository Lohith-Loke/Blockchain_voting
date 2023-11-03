# Generated by Django 4.2.6 on 2023-11-02 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d', models.CharField(auto_created=True, blank=True, default=None, editable=False, max_length=10000)),
                ('n', models.CharField(auto_created=True, blank=True, default=None, editable=False, max_length=10000)),
                ('e', models.CharField(auto_created=True, blank=True, default=None, editable=False, max_length=10000)),
                ('code', models.IntegerField(auto_created=True, default=None, editable=False, unique=True)),
                ('name', models.CharField(max_length=12)),
                ('party', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('sign', models.CharField(max_length=1024, primary_key=True, serialize=False)),
                ('m_blind', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hasvoted', models.BooleanField(auto_created=True, blank=True, default=False, editable=False)),
                ('name', models.CharField(max_length=200)),
                ('constituency', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=15)),
            ],
        ),
    ]
