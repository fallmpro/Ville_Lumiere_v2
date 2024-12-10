
from django.http import HttpResponse
from django.shortcuts import render
from .models import Team, Match, Ranking
import requests


# URL de l'API (remplace par ta clé API et ton URL)
API_KEY = '8c6d376d01062e1585c4f7df05280b64'
BASE_URL = 'https://v3.football.api-sports.io/'



# Vue pour la page principale
# Vue pour la page principale
def home(request):
    # URL de l'API pour récupérer les derniers résultats
    url = f"{BASE_URL}/fixtures"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    params = {
        'league': 61, 
        'season': 2022 
    }
    response = requests.get(url, headers=headers, params=params)
    
    # Vérification du statut de la réponse
    if response.status_code == 200:
        data = response.json()
        matches = data.get('response', [])  # Les données de match sont dans cette clé
    else:
        matches = []
    
    return render(request, 'home.html', {'matches': matches})

def teams_view(request):
    teams = Team.objects.all()
    return render(request, 'teams.html', {'teams': teams})

def matches_view(request):
    matches = Match.objects.all().order_by('-match_date')
    return render(request, 'matches.html', {'matches': matches})

def ranking_view(request):
    ranking = Ranking.objects.all().order_by('-points', '-goal_difference')
    return render(request, 'ranking.html', {'ranking': ranking})


def get_football_results(request):
    url = f"{BASE_URL}/fixtures"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    params = {
        'league': 61, 
        'season': 2022 
    }
    response = requests.get(url, headers=headers, params=params)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.json()}")
    
    if response.status_code == 200:
        data = response.json()
        matches = data.get('response', [])  # Les données se trouvent généralement ici
        print(f"Matches Data: {matches}")
        return render(request, 'football_results.html', {'matches': matches})
    else:
        return HttpResponse("Erreur lors de la récupération des données de l'API.", status=500)
    
def get_ranking(request):
    ranking_url = 'https://api-football-v1.p.rapidapi.com/v3/standings'
    params = {'season': '2022', 'league': '61'}
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    response = requests.get(ranking_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        standings = data['response'][0]['league']['standings']
        return render(request, 'ranking.html', {'standings': standings})
    else:
        return HttpResponse("Erreur lors de la récupération du classement.", status=500)

def get_matches(request):
    matches_url = 'https://api-football-v1.p.rapidapi.com/v3/fixtures'
    params = {'season': '2022', 'league': '61', 'timezone': 'Europe/Paris'}
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    response = requests.get(matches_url, headers=headers, params=params)

    if response.status_code == 200:
        matches = response.json()['response']
        return render(request, 'matches.html', {'matches': matches})
    else:
        return HttpResponse("Erreur lors de la récupération des matchs.", status=500)

def get_players(request):
    players_url = 'https://api-football-v1.p.rapidapi.com/v3/players'
    params = {'team': 'team_id', 'season': '2022'}
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    response = requests.get(players_url, headers=headers, params=params)

    if response.status_code == 200:
        players = response.json()['response']
        return render(request, 'players.html', {'players': players})
    else:
        return HttpResponse("Erreur lors de la récupération des joueurs.", status=500)

def get_teams(request):
    teams_url = 'https://api-football-v1.p.rapidapi.com/v3/teams'
    params = {'league': '61', 'season': '2022'}
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    response = requests.get(teams_url, headers=headers, params=params)

    if response.status_code == 200:
        teams = response.json()['response']
        return render(request, 'teams.html', {'teams': teams})
    else:
        return HttpResponse("Erreur lors de la récupération des équipes.", status=500)
