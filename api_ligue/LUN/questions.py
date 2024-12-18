import random

def get_questions():
    """Renvoie une liste de questions avec leurs choix et la bonne réponse."""
    questions = [
        {
            "question_text": "Quel club a remporté le plus de titres de Ligue 1 ?",
            "choices": ["Paris Saint-Germain", "Olympique de Marseille", "AS Saint-Étienne", "Olympique Lyonnais"],
            "correct_choice": 2,  # AS Saint-Étienne
        },
        {
            "question_text": "Quel est le stade du Paris Saint-Germain ?",
            "choices": ["Parc des Princes", "Stade Vélodrome", "Groupama Stadium", "Stade de France"],
            "correct_choice": 0,  # Parc des Princes
        },
        {
            "question_text": "Quel joueur détient le record de buts en Ligue 1 ?",
            "choices": ["Jean-Pierre Papin", "Delio Onnis", "Kylian Mbappé", "Thierry Henry"],
            "correct_choice": 1,  # Delio Onnis
        },
        {
            "question_text": "Quel club a remporté la Ligue 1 en 2021 ?",
            "choices": ["Lille OSC", "Paris Saint-Germain", "Olympique de Marseille", "AS Monaco"],
            "correct_choice": 0,  # Lille OSC
        },
        {
            "question_text": "Quel est le surnom de l'AS Saint-Étienne ?",
            "choices": ["Les Verts", "Les Phocéens", "Les Dogues", "Les Canaris"],
            "correct_choice": 0,  # Les Verts
        },
        {
            "question_text": "Quelle équipe joue ses matchs au Groupama Stadium ?",
            "choices": ["AS Monaco", "Olympique Lyonnais", "OGC Nice", "RC Strasbourg"],
            "correct_choice": 1,  # Olympique Lyonnais
        },
        {
            "question_text": "Qui a été élu meilleur joueur de Ligue 1 en 2022 ?",
            "choices": ["Lionel Messi", "Kylian Mbappé", "Neymar Jr", "Dimitri Payet"],
            "correct_choice": 1,  # Kylian Mbappé
        },
        {
            "question_text": "Quel est le derby le plus célèbre en Ligue 1 ?",
            "choices": ["Lyon - Saint-Étienne", "Paris - Marseille", "Monaco - Nice", "Lille - Lens"],
            "correct_choice": 1,  # Paris - Marseille
        },
        {
            "question_text": "Quel club a été relégué en Ligue 2 en 2022 ?",
            "choices": ["Bordeaux", "Saint-Étienne", "Metz", "Tous les trois"],
            "correct_choice": 3,  # Tous les trois
        },
        {
            "question_text": "Quel joueur français a été formé à l'Olympique Lyonnais ?",
            "choices": ["Zinédine Zidane", "Karim Benzema", "Paul Pogba", "Antoine Griezmann"],
            "correct_choice": 1,  # Karim Benzema
        },
    ]

    random.shuffle(questions)  # Mélange les questions
    return questions

    
    random.shuffle(questions)  # Mélange les questions
    return questions
