# Generated by Django 4.1.7 on 2023-03-05 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_room_participants'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-updated', 'created']},
        ),
    ]
