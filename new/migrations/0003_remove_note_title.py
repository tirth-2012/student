# Generated by Django 5.1.4 on 2025-02-03 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new', '0002_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='title',
        ),
    ]
