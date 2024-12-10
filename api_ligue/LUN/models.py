from django.db import models
from django.utils import timezone

# Table pour les équipes
class Team(models.Model):
    name = models.CharField(max_length=100, default="N/A")
    city = models.CharField(max_length=100, default="Inconnu")
    founded_year = models.IntegerField(default=timezone.now().year)

    def __str__(self):
        return self.name

# Table pour les joueurs
class Player(models.Model):
    team = models.ForeignKey(Team, related_name='players', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    height = models.FloatField()
    weight = models.FloatField()

    def __str__(self):
        return self.team_name

class Match(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    home_team_score = models.IntegerField(default=0)
    away_team_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name} on {self.date}"

# Table pour les statistiques de matchs
class MatchStat(models.Model):
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

    def __str__(self):
        return f"{self.team} - {self.points} pts"
