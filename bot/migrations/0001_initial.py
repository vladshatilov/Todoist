# Generated by Django 4.0.3 on 2022-06-12 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.BigIntegerField(unique=True, verbose_name='id')),
                ('user_ud', models.BigIntegerField(verbose_name='user_id')),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='связанный пользователь')),
            ],
            options={
                'verbose_name': 'tg user',
                'verbose_name_plural': 'tg users',
            },
        ),
    ]
