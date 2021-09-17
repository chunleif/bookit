# Generated by Django 3.2.4 on 2021-06-29 04:44

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Court',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CName', models.CharField(max_length=200)),
                ('CType', models.IntegerField(null=True)),
                ('CAddress', models.CharField(max_length=200)),
                ('RPId', models.IntegerField(null=True)),
                ('CIntro', ckeditor.fields.RichTextField()),
                ('CStar', models.IntegerField(null=True)),
                ('CStatus', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TypeName', models.CharField(max_length=200)),
                ('TypeAvailable', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('phonenumber', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ResourceConsumers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RCName', models.CharField(max_length=200)),
                ('RCEmail', models.CharField(max_length=200)),
                ('RCPassword', models.CharField(max_length=200)),
                ('permitHour', models.IntegerField(default=10)),
                ('RCPhone', models.CharField(max_length=50)),
                ('RCIsActive', models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResourceProviders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RPName', models.CharField(max_length=200)),
                ('RPEmail', models.CharField(max_length=200)),
                ('RPPassword', models.CharField(max_length=200)),
                ('RPPhone', models.CharField(max_length=50)),
                ('RPIntro', ckeditor.fields.RichTextField()),
                ('RPIsActive', models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CId', models.IntegerField(null=True)),
                ('Week', models.IntegerField(null=True)),
                ('Hour', models.IntegerField(null=True)),
                ('Available', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VerificationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('VCText', models.CharField(max_length=10)),
                ('VCGeneralTime', models.DateTimeField(null=True)),
                ('UserRole', models.CharField(max_length=10)),
                ('UserEmail', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OrderTime', models.DateTimeField(auto_now_add=True)),
                ('ScheduleTime', models.CharField(max_length=200)),
                ('OrderStatus', models.IntegerField(null=True)),
                ('CId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.court')),
                ('RCId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.resourceconsumers')),
            ],
        ),
    ]
