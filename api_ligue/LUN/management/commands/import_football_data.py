import requests
from django.core.management.base import BaseCommand
from LUN.models import Ranking, MatchStat, Team, Player, Match
import time


# Remplacez avec vos clés et URL
API_KEY = '90f3bbf796250f039530e422edc524ae'
BASE_URL = 'https://v3.football.api-sports.io'

HEADERS = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': 'v3.football.api-sports.io'
}

class Command(BaseCommand):
    help = "Importe les données football de l'API et les stocke dans la base de données"

    def handle(self, *args, **kwargs):
        self.stdout.write("Début de l'importation des équipes")
        self.import_teams()
        self.stdout.write("Équipes importées")
    
        self.stdout.write("Début de l'importation des classements")
        self.import_rankings()
        self.stdout.write("Classements importés")
    #    self.import_players()
    #    self.import_matches()
    #    self.import_match_stats()

    def import_teams(self):
        self.stdout.write("Appel de la fonction import_teams")
        url = f"{BASE_URL}/teams"
        params = {'league': 61, 'season': 2022}
        response = requests.get(url, headers=HEADERS, params=params)
        self.stdout.write(str(response.json()))

        
        if response.status_code == 200:
            teams = response.json().get('response', [])
            for team_data in teams:
                team_info = team_data['team']
                team_venue = team_data.get('venue', {}) 

                self.stdout.write(f"Traitement de l'équipe : {team_info.get('name', 'Inconnue')}")
                self.stdout.write(f"Ville : {team_venue.get('city', 'Inconnu')}, Fondée : {team_info.get('founded', 'Non disponible')}")

                try:
                    team, created = Team.objects.update_or_create(
                        api_id=team_info['id'],  
                        defaults={
                            'name': team_info['name'],
                            'logo': team_info.get('logo', "https://via.placeholder.com/150"),
                            'country': team_info.get('country', "Unknown"),
                            'city': team_venue.get('city', "Inconnu"),
                            'founded_year': team_info.get('founded', None) or 0,
                        }
                    )
                    self.stdout.write(f"Équipe {'créée' if created else 'mise à jour'}: {team.name}")
                except Exception as e:
                    self.stderr.write(f"Erreur lors de l'import de l'équipe {team_info['name']}: {str(e)}")
        else:
            self.stderr.write(f"Erreur lors de la récupération des équipes: {response.status_code}")
    

    def import_rankings(self):
        self.stdout.write("Appel de la fonction import_ranking")
        url = f"{BASE_URL}/standings"
        params = {'league': 61, 'season': 2022}  # Exemple : Ligue 1, saison 2022
        response = requests.get(url, headers=HEADERS, params=params)

        if response.status_code == 200:
            standings = response.json().get('response', [])
            if standings:
                for team_data in standings[0]['league']['standings'][0]:
                    team = Team.objects.filter(api_id=team_data['team']['id']).first()
                    if team:
                        Ranking.objects.update_or_create(
                            team=team,
                            defaults={
                                'points': team_data['points'],
                                'position': team_data['rank'],
                                'goal_difference': team_data['goalsDiff'],
                            }
                        )
                        self.stdout.write(f"Classement mis à jour pour l'équipe : {team.name}")
        else:
            self.stderr.write(f"Erreur lors de la récupération du classement : {response.status_code}")

"""
commande pas utile car bdd complete

    def import_players(self):
        url = f"{BASE_URL}/players"
        params = {'league': 61, 'season': 2022}
        response = requests.get(url, headers=HEADERS, params=params)

        if response.status_code == 200:
            players = response.json().get('response', [])
            for player_data in players:
                team = Team.objects.filter(api_id=player_data['statistics'][0]['team']['id']).first()
                if team:
                    Player.objects.update_or_create(
                        api_id=player_data['player']['id'],  # Utilisation du champ `api_id`
                        defaults={
                            'first_name': player_data['player']['firstname'],
                            'last_name': player_data['player']['lastname'],
                            'position': player_data['statistics'][0]['games']['position'],
                            'date_of_birth': player_data['player']['birth']['date'],
                            'nationality': player_data['player']['nationality'],
                            'height': float(player_data['player']['height'].strip().replace(' cm', '')) 
                                if player_data['player']['height'] and player_data['player']['height'].strip().replace(' cm', '').isdigit() 
                                else None,
                            'weight': float(player_data['player']['weight'].replace(' kg', '')) 
                                if player_data['player']['weight'] and player_data['player']['weight'].strip().replace(' kg', '').isdigit()
                                else None,
                            'team': team,
                        }
                    )
                    self.stdout.write(f"Joueur importé: {player_data['player']['firstname']} {player_data['player']['lastname']}")
        else:
            self.stderr.write(f"Erreur lors de la récupération des joueurs: {response.status_code}")

    def import_matches(self):
        url = f"{BASE_URL}/fixtures"
        params = {'league': 61, 'season': 2022}  # Exemple : Ligue 1, saison 2022
        response = requests.get(url, headers=HEADERS, params=params)

        if response.status_code == 200:
            matches = response.json().get('response', [])
            for match_data in matches:
                home_team = Team.objects.filter(api_id=match_data['teams']['home']['id']).first()
                away_team = Team.objects.filter(api_id=match_data['teams']['away']['id']).first()
                if home_team and away_team:
                    Match.objects.update_or_create(
                        api_id=match_data['fixture']['id'],  # Assurez-vous que le champ api_id existe dans Match
                        defaults={
                            'date': match_data['fixture']['date'],
                            'home_team': home_team,
                            'away_team': away_team,
                            'home_team_score': match_data['goals']['home'] if match_data['goals']['home'] is not None else 0,
                            'away_team_score': match_data['goals']['away'] if match_data['goals']['away'] is not None else 0,
                        }
                    )
                    self.stdout.write(
                        f"Match importé : {home_team.name} vs {away_team.name} ({match_data['fixture']['date']})"
                    )
        else:
            self.stderr.write(f"Erreur lors de la récupération des matchs : {response.status_code}")
    
    def import_match_stats(self):
        
        #Importe les statistiques des joueurs pour chaque match existant dans la base de données.
        
        matches = Match.objects.all()  # Récupère tous les matchs déjà importés
        for i, match in enumerate(matches):
            self.stdout.write(f"Traitement du match {i + 1}/{matches.count()} : {match}")

            url = f"{BASE_URL}/fixtures/players"
            params = {'fixture': match.api_id}  # Utilise l'ID API du match
            response = requests.get(url, headers=HEADERS, params=params)

            if response.status_code == 200:
                stats_data = response.json().get('response', [])
                for team_entry in stats_data:
                    for stat_entry in team_entry.get('players', []):
                        player_data = stat_entry.get('player')
                        stats = stat_entry.get('statistics', [{}])[0]  # Sécurise l'accès aux statistiques

                        # Vérifie que les données du joueur et des statistiques existent
                        if not player_data or not stats:
                            self.stderr.write(f"Données incomplètes pour le match {match.api_id}: {stat_entry}")
                            continue

                        # Récupère le joueur correspondant dans la base
                        player = Player.objects.filter(api_id=player_data['id']).first()
                        if player:
                            # Gère les statistiques manquantes avec des valeurs par défaut
                            MatchStat.objects.update_or_create(
                                match=match,
                                player=player,
                                defaults={
                                    'goals': stats.get('goals', {}).get('total', 0) or 0,
                                    'assists': stats.get('goals', {}).get('assists', 0) or 0,
                                    'yellow_cards': stats.get('cards', {}).get('yellow', 0) or 0,
                                    'red_cards': stats.get('cards', {}).get('red', 0) or 0,
                                    'minutes_played': stats.get('games', {}).get('minutes', 0) or 0,
                                }
                            )
                            self.stdout.write(f"Stats ajoutées pour {player.first_name} {player.last_name} dans le match {match}")
                        else:
                            self.stderr.write(f"Joueur introuvable pour les données : {player_data}")
            else:
                self.stderr.write(f"Erreur lors de la récupération des stats pour le match {match.api_id} : {response.status_code}")

            # Pause pour éviter les limites de l'API
            time.sleep(1)
"""
