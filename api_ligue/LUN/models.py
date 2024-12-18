from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Team(models.Model):
    api_id = models.IntegerField(unique=True, null=True, default=0)
    name = models.CharField(max_length=100, default="N/A")
    city = models.CharField(max_length=100, default="Inconnu")
    founded_year = models.IntegerField(default=timezone.now().year)
    country = models.CharField(max_length=100, null=True, blank=True, default="Unknown")  
    logo = models.URLField(null=True, blank=True, default="https://via.placeholder.com/150")  

    def __str__(self):
        return self.name

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


    def get_recent_matches(self):
        return Match.objects.filter(home_team=self) | Match.objects.filter(away_team=self)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField('Team', blank=True, related_name='favorited_by')

    def __str__(self):
        return f"Profil de {self.user.username}"


# Table pour les joueurs
class Player(models.Model):
    api_id = models.IntegerField(unique=True, null=True, default=0)  # Nouveau champ pour l'ID API
    team = models.ForeignKey(Team, related_name='players', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    height = models.FloatField(null=True,blank=True,default=0)
    weight = models.FloatField(null=True,blank=True,default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.team.name})"


class Match(models.Model):
    api_id = models.IntegerField(unique=True, null=True)  # Champ pour identifier le match unique
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    home_team_score = models.IntegerField(default=0)
    away_team_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name} on {self.date}"


# Table pour les statistiques de matchs
class MatchStat(models.Model):
    api_id = models.IntegerField(unique=True, null=True, default=None)  # ID unique depuis l'API
    match = models.ForeignKey(Match, related_name='stats', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='stats', on_delete=models.CASCADE)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    minutes_played = models.IntegerField()

    def __str__(self):
        return f"Stats for {self.player} in {self.match}"


# Table pour le classement des équipes
class Ranking(models.Model):
    team = models.ForeignKey(Team, related_name='rankings', on_delete=models.CASCADE)
    points = models.IntegerField()
    position = models.IntegerField(default=1)
    goal_difference = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.team} - {self.points} pts"
