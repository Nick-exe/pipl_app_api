# Generated by Django 3.1.6 on 2021-02-15 23:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_note_pip_reminder'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='owner',
            new_name='user',
        ),
        migrations.AddField(
            model_name='pip',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reminder',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.user'),
            preserve_default=False,
        ),
    ]
