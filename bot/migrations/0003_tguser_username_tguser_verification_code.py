# Generated by Django 4.0.3 on 2022-06-18 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_rename_bot_tguser'),
    ]

    operations = [
        migrations.AddField(
            model_name='tguser',
            name='username',
            field=models.CharField(blank=True, default=None, max_length=512, null=True, verbose_name='username'),
        ),
        migrations.AddField(
            model_name='tguser',
            name='verification_code',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='verification_code_handler'),
        ),
    ]