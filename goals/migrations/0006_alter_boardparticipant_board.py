# Generated by Django 4.0.3 on 2022-06-05 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0005_alter_goalcategory_board'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardparticipant',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='board_participants', to='goals.board', verbose_name='Доска'),
        ),
    ]
