# Generated by Django 3.1.7 on 2021-02-19 16:12

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210217_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='pip',
            name='image',
            field=models.ImageField(null=True, upload_to=core.models.pipl_image_file_path),
        ),
    ]
