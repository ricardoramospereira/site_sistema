# Generated by Django 4.2.7 on 2023-12-22 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_postagemforumimagem'),
    ]

    operations = [
        migrations.AddField(
            model_name='postagemforum',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
