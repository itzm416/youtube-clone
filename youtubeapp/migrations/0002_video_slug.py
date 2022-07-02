# Generated by Django 4.0.1 on 2022-02-02 22:04

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youtubeapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, null=True, populate_from='video_title', unique=True),
        ),
    ]
