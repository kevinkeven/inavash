# Generated by Django 2.2.5 on 2020-04-26 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
