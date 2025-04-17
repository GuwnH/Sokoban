from django.db import migrations

def seed_games(apps, schema_editor):
    Game = apps.get_model('guides', 'Game')
    
    if not Game.objects.exists():
        Game.objects.create(
            game_name="Sokoban Classic",
            number_levels=10,
            weighted_ratings=4.5,
            additional_inputs=False
        )
        Game.objects.create(
            game_name="Sokoban Extreme",
            number_levels=20,
            weighted_ratings=4.8,
            additional_inputs=True
        )
        Game.objects.create(
            game_name="Snails & Sorcery",
            number_levels=10,
            weighted_ratings=4.5,
            additional_inputs=True
        )

class Migration(migrations.Migration):

    dependencies = [
        ('guides', '0002_alter_image_user_alter_guide_user_userprofile_and_more'), 
    ]

    operations = [
        migrations.RunPython(seed_games),
    ]