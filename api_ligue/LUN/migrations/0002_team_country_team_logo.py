# Generated by Django 5.0.6 on 2024-12-10 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LUN', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='country',
            field=models.CharField(blank=True, default='Unknown', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='logo',
            field=models.URLField(blank=True, default='https://via.placeholder.com/150', null=True),
        ),
    ]