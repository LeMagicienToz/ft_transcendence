# Generated by Django 5.1.1 on 2024-11-08 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_app', '0005_game_game_custom_name_game_score_to_win_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='tournament_custom_name',
            field=models.CharField(default='tournament_custom_name', max_length=30),
        ),
    ]