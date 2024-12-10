from django.contrib import admin
from django.db.models import F
from .models import Match, Team, Ranking

# --- Admin pour Match ---
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'date', 'home_team_goals', 'away_team_goals')  # Utilisation de 'date' au lieu de 'match_date'
    list_filter = ('date', 'home_team', 'away_team')  # Utilisation de 'date' au lieu de 'match_date'
    search_fields = ('home_team__name', 'away_team__name')

    def home_team_goals(self, obj):
        return obj.home_team_score
    home_team_goals.short_description = 'Home Team Goals'

    def away_team_goals(self, obj):
        return obj.away_team_score
    away_team_goals.short_description = 'Away Team Goals'

# --- Admin pour Ranking ---
class RankingAdmin(admin.ModelAdmin):
    list_display = ('team', 'played', 'won', 'drawn', 'lost', 'goals_for', 'goals_against', 'goal_difference', 'points')
    list_filter = ('team',)

    def played(self, obj):
        return obj.matches.count()

    def won(self, obj):
        return obj.matches.filter(home_team_score__gt=F('away_team_score')).count()  # Correction du champ

    def drawn(self, obj):
        return obj.matches.filter(home_team_score=F('away_team_score')).count()  # Correction du champ

    def lost(self, obj):
        return obj.matches.filter(home_team_score__lt=F('away_team_score')).count()  # Correction du champ

    def goals_for(self, obj):
        return sum([match.home_team_score for match in obj.matches.all()])  # Correction du champ

    def goals_against(self, obj):
        return sum([match.away_team_score for match in obj.matches.all()])  # Correction du champ

    def goal_difference(self, obj):
        return self.goals_for(obj) - self.goals_against(obj)

    def points(self, obj):
        return (self.won(obj) * 3) + (self.drawn(obj) * 1)

# --- Admin pour Team ---
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'founded_year')
    search_fields = ('name', 'city')
    ordering = ('name',)

admin.site.register(Match, MatchAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Ranking, RankingAdmin)
