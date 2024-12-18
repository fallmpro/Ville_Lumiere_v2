from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from .models import Team, Match, Ranking
from .forms import SignUpForm
import requests

# URL de l'API (remplace par ta clé API et ton URL)
API_KEY = '4e1c0aee9fb2abbb18aae9091a28de5c'
BASE_URL = 'https://v3.football.api-sports.io/'

# Vue pour la page principale
def home(request):
    return render(request, 'home.html')

def teams_view(request):
    teams = Team.objects.all()
    return render(request, 'equipes.html', {'teams': teams})

def matches_view(request):
    matches = Match.objects.all().order_by('-match_date')
    return render(request, 'matches.html', {'matches': matches})

def ranking_view(request):
    ranking = Ranking.objects.all().order_by('-points', '-goal_difference')
    print(ranking)
    return render(request, 'ranking.html', {'ranking': ranking})

def football_results(request):
    filter_type = request.GET.get('filter', 'all')  # Par défaut, afficher tous les matchs
    team_name = request.GET.get('team', '').strip()  # Filtrer par nom d'équipe (facultatif)

    # Base query : tous les matchs
    matches = Match.objects.all().order_by('-date')

    # Filtrer par équipe si un nom est fourni
    if team_name:
        matches = matches.filter(
            Q(home_team__name__icontains=team_name) | Q(away_team__name__icontains=team_name)
        )

    # Appliquer le filtre sur le nombre de matchs
    if filter_type == '5_last':
        matches = matches[:5]
    elif filter_type == '15_last':
        matches = matches[:15]

    return render(request, 'football_results.html', {
        'matches': matches,
        'filter_type': filter_type,
        'team_name': team_name
    })

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


from django.shortcuts import render

def quizz_view(request):
    # Questions et réponses du quiz
    questions = [
        {
            'question': "Quelle équipe a remporté la Coupe du Monde 2018 ?",
            'choices': ["Allemagne", "Brésil", "France", "Argentine"],
            'correct': "France",
        },
        {
            'question': "Qui est le meilleur buteur de l'histoire de la Ligue des Champions ?",
            'choices': ["Cristiano Ronaldo", "Lionel Messi", "Robert Lewandowski", "Karim Benzema"],
            'correct': "Cristiano Ronaldo",
        },
        {
            'question': "Combien de joueurs sont sur le terrain dans une équipe de football ?",
            'choices': ["9", "10", "11", "12"],
            'correct': "11",
        },
        {
            'question': "Quel pays organise la Coupe du Monde 2026 ?",
            'choices': ["Canada, Mexique et États-Unis", "Angleterre", "Qatar", "Allemagne"],
            'correct': "Canada, Mexique et États-Unis",
        },
        {
            'question': "Quel joueur a remporté le Ballon d'Or 2023 ?",
            'choices': ["Lionel Messi", "Erling Haaland", "Kylian Mbappé", "Robert Lewandowski"],
            'correct': "Lionel Messi",
        },
    ]

    results = None
    if request.method == "POST":
        user_answers = [request.POST.get(f"question_{i}") for i in range(len(questions))]
        results = [
            {
                'question': q['question'],
                'user_answer': user_answers[i],
                'correct_answer': q['correct'],
                'is_correct': user_answers[i] == q['correct'],
            }
            for i, q in enumerate(questions)
        ]

    return render(request, 'quizz.html', {'questions': questions, 'results': results})
