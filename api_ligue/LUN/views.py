from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Team, Match, Ranking
from .forms import SignUpForm
from django.contrib import messages
import requests


# URL de l'API (remplace par ta clé API et ton URL)
API_KEY = '8c6d376d01062e1585c4f7df05280b64'
BASE_URL = 'https://v3.football.api-sports.io/'




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

def ranking_view(request):
    rankings = Ranking.objects.all().order_by('position')
    return render(request, 'ranking.html', {'rankings': rankings})

    
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
        standings = []

        # Récupère les données pour chaque équipe
        for team_data in data['response'][0]['league']['standings'][0]:
            standings.append({
                'position': team_data['rank'],
                'team_name': team_data['team']['name'],
                'points': team_data['points'],
                'goal_difference': team_data['goalsDiff'],  # Assure-toi que c'est la bonne clé
                'logo': team_data['team']['logo'],  # Ajout du logo si besoin
            })

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
    search_query = request.GET.get('nom', '')
    filter_type = request.GET.get('filter', 'all')  # Par défaut, "all"
    team = Team.objects.filter(name__icontains=search_query).first() if search_query else None
    matches = []

    if search_query:
        team = Team.objects.filter(name__icontains=search_query).first()
        if team:
            if filter_type == 'home':
                matches = Match.objects.filter(home_team=team).order_by('-date')[:10]
            elif filter_type == 'away':
                matches = Match.objects.filter(away_team=team).order_by('-date')[:10]
            else:  # 'all'
                matches = Match.objects.filter(home_team=team) | Match.objects.filter(away_team=team)
                matches = matches.order_by('-date')[:10]

    return render(request, 'equipes.html', {
        'team': team,
        'matches': matches,
        'search_query': search_query,
        'filter_type': filter_type,
    })

# Vue pour l'inscription
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistre l'utilisateur dans la BDD
            messages.success(request, "Votre compte a été créé avec succès. Vous pouvez maintenant vous connecter.")
            return redirect('login')  # Redirige vers la page de connexion
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = UserCreationForm()
    
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

@login_required
def add_favorite(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    request.user.profile.favorites.add(team)
    return redirect('ranking')

@login_required
def remove_favorite(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    request.user.profile.favorites.remove(team)
    return redirect('ranking')


def quizz(request):
    """
    Mathys modifie
    """
    return render(request, 'quizz.html', {'message': 'Le quizz arrive bientôt !'})