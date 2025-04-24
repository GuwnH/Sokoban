from django.db import models
from django.contrib.auth.models import User

# class User(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     user_name = models.CharField(max_length=30)
#     user_pass = models.CharField(max_length=30)
#     user_email = models.CharField(max_length=60)
#     user_display = models.CharField(max_length=60, blank=True, null=True)
#     def __str__(self):
#         return f"{self.user_name} ({self.user_email})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_display = models.CharField(max_length=60, blank=True, null=True)

class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=60)
    number_levels = models.IntegerField()
    weighted_ratings = models.DecimalField(max_digits=3, decimal_places=2)
    additional_inputs = models.BooleanField()

class Guide(models.Model):
    guide_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    guide_level = models.IntegerField()
    guide_text = models.CharField(max_length=10000)
    number_of_moves = models.IntegerField()
    colors_required = models.BooleanField()

class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
