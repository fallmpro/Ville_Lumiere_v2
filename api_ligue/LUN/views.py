from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render , redirect, get_object_or_404
from .models import Team, Match, Ranking
from .forms import SignUpForm
import requests


# URL de l'API (remplace par ta clé API et ton URL)
API_KEY = '8c6d376d01062e1585c4f7df05280b64'
BASE_URL = 'https://v3.football.api-sports.io/'



# Vue pour la page principale
# Vue pour la page principale
# Vue pour la page principale
def home(request):
    # URL pour récupérer les résultats des matchs
    url_matches = f"{BASE_URL}/fixtures"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    params_matches = {
        'league': 61, 
        'season': 2022 
    }
    response_matches = requests.get(url_matches, headers=headers, params=params_matches)

    if response_matches.status_code == 200:
        data_matches = response_matches.json()
        matches = data_matches.get('response', [])
    else:
        matches = []

    # URL pour récupérer les équipes
    url_teams = f"{BASE_URL}/teams"
    params_teams = {
        'league': 61,
        'season': 2022
    }
    response_teams = requests.get(url_teams, headers=headers, params=params_teams)

    if response_teams.status_code == 200:
        data_teams = response_teams.json()
        teams = data_teams.get('response', [])
    else:
        teams = []

    return render(request, 'home.html', {'matches': matches, 'teams': teams})
def teams_view(request):
    teams = Team.objects.all()
    return render(request, 'equipes.html', {'teams': teams})

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

def equipe_detail(request):
    # Récupération de l'équipe recherchée depuis le paramètre GET
    team_name = request.GET.get('nom', None)
    team = None
    matches = None

    if team_name:
        try:
            # Recherche de l'équipe dans la base de données (recherche insensible à la casse)
            team = Team.objects.get(name__icontains=team_name)

            # Récupération des matchs associés (comme équipe à domicile ou à l'extérieur)
            matches = Match.objects.filter(home_team=team) | Match.objects.filter(away_team=team)
            matches = matches.order_by('-date')  # Trier par date décroissante
        except Team.DoesNotExist:
            # Si aucune équipe n'est trouvée, on laisse `team` à None
            team = None

    context = {
        'team': team,
        'matches': matches,
        'search_query': team_name,
        'error': f"Aucune équipe trouvée pour '{team_name}'." if not team and team_name else None,
    }
    return render(request, 'equipes.html', context)




# Vue pour l'inscription
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # Crée l'utilisateur
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)  # Authentifie l'utilisateur
            login(request, user)  # Connecte l'utilisateur automatiquement
            return redirect('home')  # Redirige vers la page d'accueil
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# Vue pour la connexion
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Connecte l'utilisateur
            return redirect('home')  # Redirige vers la page d'accueil
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Vue pour la déconnexion
def logout_view(request):
    logout(request)  # Déconnecte l'utilisateur
    return redirect('home')