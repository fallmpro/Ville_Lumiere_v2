from django.contrib import admin
from .models import Team, Match, Ranking

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'team_name')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'home_team', 'away_team', 'home_team_goals', 'away_team_goals', 'match_date')
    list_filter = ('match_date', 'home_team', 'away_team')

@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    list_display = ('team', 'played', 'won', 'drawn', 'lost', 'goals_for', 'goals_against', 'goal_difference', 'points')
    list_filter = ('points', 'goal_difference')
