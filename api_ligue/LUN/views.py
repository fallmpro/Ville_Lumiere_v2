
from django.http import HttpResponse
from django.shortcuts import render
from .models import Team, Match, Ranking


# Vue pour la page principale
def home(request):
    return render(request, 'home.html')

def teams_view(request):
    teams = Team.objects.all()
    return render(request, 'teams.html', {'teams': teams})

def matches_view(request):
    matches = Match.objects.all().order_by('-match_date')
    return render(request, 'matches.html', {'matches': matches})

def ranking_view(request):
    ranking = Ranking.objects.all().order_by('-points', '-goal_difference')
    return render(request, 'ranking.html', {'ranking': ranking})
