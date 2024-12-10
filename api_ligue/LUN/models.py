from django.db import models

class Team(models.Model):
    team_name = models.CharField(max_length=255)

    def __str__(self):
        return self.team_name
    


class Team(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='team_logos/')
    description = models.TextField(blank=True)


class Match(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    home_team_goals = models.IntegerField()
    away_team_goals = models.IntegerField()
    match_date = models.DateField()

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.match_date}"

class Ranking(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    played = models.IntegerField(default=0)
    won = models.IntegerField(default=0)
    drawn = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    goal_difference = models.IntegerField(editable=False, default=0)
    points = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.goal_difference = self.goals_for - self.goals_against
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.team} - {self.points} pts"
    
    
