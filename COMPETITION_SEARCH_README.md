# 🏆 Système de Recherche de Compétitions FFE

## 📋 Description

Ce module ajoute un système de recherche automatique des compétitions FFE depuis le site ffecompet.ffe.com. Il permet de :

- Rechercher des compétitions CSO/Obstacle dans le Nord, Normandie et Île-de-France
- Filtrer par discipline, région, niveau et dates
- Programmer des recherches automatiques avec notifications email
- Marquer des compétitions comme favorites
- Créer des entrées de compétition directement depuis les résultats

## 🚀 Fonctionnalités

### ✅ Recherche Manuelle
- Interface conviviale pour définir des critères de recherche
- Filtres par discipline (CSO, Dressage, Complet, etc.)
- Sélection de région (Hauts-de-France, Normandie, Île-de-France)
- Filtrage par niveau (Club, Amateur, Pro, International)
- Plage de dates personnalisable

### ✅ Recherche Automatique
- Recherches programmées hebdomadaires
- Notifications email automatiques
- Historique des recherches
- Suivi des nouvelles compétitions

### ✅ Gestion des Résultats
- Liste des compétitions trouvées avec détails complets
- Marquage des favoris
- Liens directs vers FFEcompet
- Création de compétitions dans Stable Manager
- Notes personnelles par compétition

## 🛠 Installation et Configuration

### 1. Dépendances Python (Optionnelles pour le scraping avancé)
```bash
pip install requests beautifulsoup4 selenium
```

### 2. Activation du Module
1. Installer le module Stable Manager
2. Les nouveaux menus apparaîtront sous "Recherche FFE"

### 3. Configuration Initiale
1. Aller dans **Recherche FFE > Mes recherches**
2. Créer une nouvelle recherche
3. Définir les critères (discipline, région, etc.)
4. Cliquer sur "🔍 Lancer la recherche"

## 📡 Implémentation du Web Scraping

### ⚠️ Note Importante
Actuellement, le module utilise des données simulées pour la démonstration. Pour une implémentation en production, vous devez :

1. **Respecter les conditions d'utilisation** de ffecompet.ffe.com
2. **Implementer un vrai système de scraping** (voir section suivante)
3. **Gérer les limitations de taux** et la politesse envers le serveur

### 🔧 Implémentation Recommandée

#### Option 1: Web Scraping Simple (BeautifulSoup)
```python
def _scrape_ffe_competitions_real(self):
    """Implémentation réelle du scraping FFE"""
    import requests
    from bs4 import BeautifulSoup
    
    competitions = []
    
    # URL de base FFEcompet (à adapter selon la vraie structure)
    base_url = "https://ffecompet.ffe.com/concours"
    
    # Paramètres de recherche
    params = {
        'discipline': self.discipline,
        'region': self.region,
        'level': self.level,
        'date_from': self.date_from,
        'date_to': self.date_to,
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Parser les résultats (à adapter selon la structure HTML réelle)
        competition_elements = soup.find_all('div', class_='competition-item')
        
        for element in competition_elements:
            competition = {
                'name': element.find('h3').text.strip(),
                'location': element.find('.location').text.strip(),
                'date_start': element.find('.date-start').text.strip(),
                'date_end': element.find('.date-end').text.strip(),
                'organizer': element.find('.organizer').text.strip(),
                'url': element.find('a')['href'],
                # ... autres champs
            }
            competitions.append(competition)
            
    except Exception as e:
        _logger.error(f"Erreur scraping FFE: {str(e)}")
        raise
        
    return competitions
```

#### Option 2: Scraping Avancé (Selenium)
Pour les sites avec beaucoup de JavaScript :

```python
def _scrape_ffe_competitions_selenium(self):
    """Scraping avec Selenium pour sites JavaScript"""
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://ffecompet.ffe.com/concours")
        
        # Remplir les formulaires de recherche
        # ... logique de navigation
        
        # Récupérer les résultats
        competitions = []
        # ... parser les résultats
        
        return competitions
        
    finally:
        driver.quit()
```

#### Option 3: API Alternative
Si FFE propose une API ou flux RSS :

```python
def _fetch_ffe_api(self):
    """Utiliser une API officielle si disponible"""
    api_url = "https://api.ffe.com/competitions"  # URL hypothétique
    
    headers = {
        'Authorization': 'Bearer YOUR_API_KEY',
        'User-Agent': 'Stable-Manager/1.0'
    }
    
    params = {
        'discipline': self.discipline,
        'region': self.region,
        'from_date': self.date_from,
        'to_date': self.date_to,
    }
    
    response = requests.get(api_url, params=params, headers=headers)
    return response.json()
```

## 🔄 Automatisation

### Configuration des Recherches Automatiques
1. Cocher "Recherche automatique" sur une recherche
2. Ajouter des emails de notification
3. Le système lancera la recherche chaque semaine automatiquement

### Cron Job
Le module inclut un cron job qui s'exécute hebdomadairement :
```xml
<record id="cron_competition_auto_search" model="ir.cron">
    <field name="name">Recherches automatiques de compétitions FFE</field>
    <field name="interval_number">1</field>
    <field name="interval_type">weeks</field>
</record>
```

## 📧 Notifications Email

Les notifications automatiques incluent :
- Liste des nouvelles compétitions trouvées
- Détails principaux (nom, lieu, date)
- Lien vers les résultats complets dans Odoo

## 🎯 Utilisation Pratique

### Workflow Recommandé
1. **Créer une recherche** pour votre région et discipline
2. **Activer la recherche automatique** avec votre email
3. **Recevoir les notifications** hebdomadaires
4. **Marquer les favoris** depuis l'interface
5. **Créer des compétitions** directement dans votre module

### Conseils d'Utilisation
- Utilisez des critères spécifiques pour éviter trop de résultats
- Configurez plusieurs recherches pour différentes disciplines
- Vérifiez régulièrement vos favoris pour les dates limites d'engagement

## ⚖️ Considérations Légales

### Respect des Conditions d'Utilisation
- Vérifiez les conditions d'utilisation de ffecompet.ffe.com
- Respectez les limitations de taux (ne pas surcharger le serveur)
- Identifiez votre application avec un User-Agent approprié

### Politesse du Scraping
```python
import time
import random

def polite_request(url):
    # Attendre entre les requêtes
    time.sleep(random.uniform(1, 3))
    
    headers = {
        'User-Agent': 'Stable-Manager/1.0 (contact@yoursite.com)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    return requests.get(url, headers=headers)
```

## 🐛 Dépannage

### Erreurs Communes
1. **Timeout de connexion** : Augmenter le timeout des requêtes
2. **Structure HTML changée** : Mettre à jour les sélecteurs CSS
3. **Blocage par détection de bot** : Améliorer les headers et ralentir les requêtes

### Logs et Debugging
Les erreurs sont loggées dans les logs Odoo :
```
_logger.error(f"Erreur scraping FFE: {str(e)}")
```

## 🔮 Améliorations Futures

### Fonctionnalités Prévues
- [ ] Intégration avec calendrier Outlook/Google
- [ ] Notifications push mobiles
- [ ] Comparaison de prix d'engagement
- [ ] Historique des performances par organisateur
- [ ] Export PDF des listes de compétitions
- [ ] Synchronisation avec planning des chevaux

### Intégrations Possibles
- **API Google Calendar** : Ajouter automatiquement les compétitions
- **SMS Notifications** : Rappels avant dates limites
- **Slack/Teams** : Notifications d'équipe
- **Waze/Google Maps** : Calcul d'itinéraires automatique

## 📞 Support

Pour toute question ou problème :
1. Vérifiez les logs Odoo
2. Consultez la documentation FFE
3. Testez d'abord avec des données simulées

---

**⚠️ Rappel Important :** Assurez-vous de respecter les conditions d'utilisation du site FFEcompet et d'implémenter un scraping responsable avant d'utiliser ce module en production.