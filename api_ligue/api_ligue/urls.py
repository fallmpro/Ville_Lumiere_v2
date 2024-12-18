"""
URL configuration for api_ligue project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from LUN.views import signup_view, login_view, logout_view, home
from django.contrib.auth import views as auth_views
from LUN import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('football-results/', views.football_results, name='football_results'),
    path('teams/', views.equipe_detail, name='equipe_detail'),
    path('matches/', views.matches_view, name='matches'),
    path('ranking/', views.ranking_view, name='ranking'),
    path('signup/', views.signup_view, name='signup'),  
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  
    path('ranking/', views.ranking_view, name='ranking'),
    path('add-favorite/<int:team_id>/', views.add_favorite, name='add_favorite'),
    path('remove-favorite/<int:team_id>/', views.remove_favorite, name='remove_favorite'),
    path('quizz/', views.quizz_view, name='quizz'),
]


