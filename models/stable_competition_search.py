from odoo import models, fields, api
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging
import json

_logger = logging.getLogger(__name__)


class StableCompetitionSearch(models.Model):
    _name = 'stable.competition.search'
    _description = 'FFE Competition Search'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'search_date desc'

    # Paramètres de recherche
    name = fields.Char("Nom de la recherche", required=True)
    search_date = fields.Datetime("Date de recherche", default=fields.Datetime.now)
    
    # Critères de recherche
    discipline = fields.Selection([
        ('cso', 'CSO/Obstacle'),
        ('dressage', 'Dressage'),
        ('complet', 'Complet'),
        ('endurance', 'Endurance'),
        ('attelage', 'Attelage'),
        ('pony_games', 'Pony Games'),
        ('equifeel', 'Equifeel'),
        ('trec', 'TREC'),
        ('voltige', 'Voltige'),
        ('horse_ball', 'Horse Ball'),
    ], string="Discipline", default='cso', required=True)
    
    region = fields.Selection([
        ('hauts-de-france', 'Hauts-de-France'),
        ('normandie', 'Normandie'),
        ('ile-de-france', 'Île-de-France'),
        ('grand-est', 'Grand Est'),
        ('bretagne', 'Bretagne'),
        ('centre-val-de-loire', 'Centre-Val de Loire'),
        ('pays-de-la-loire', 'Pays de la Loire'),
        ('bourgogne-franche-comte', 'Bourgogne-Franche-Comté'),
        ('nouvelle-aquitaine', 'Nouvelle-Aquitaine'),
        ('auvergne-rhone-alpes', 'Auvergne-Rhône-Alpes'),
        ('occitanie', 'Occitanie'),
        ('provence-alpes-cote-azur', 'Provence-Alpes-Côte d\'Azur'),
        ('corse', 'Corse'),
        ('outre-mer', 'Outre-mer'),
    ], string="Région")
    
    level = fields.Selection([
        ('club', 'Club'),
        ('poney', 'Poney'),
        ('amateur', 'Amateur'),
        ('pro', 'Pro'),
        ('international', 'International'),
    ], string="Niveau")
    
    date_from = fields.Date("Date de début", default=fields.Date.today)
    date_to = fields.Date("Date de fin", default=lambda self: fields.Date.today() + timedelta(days=90))
    
    # Résultats de recherche
    competition_ids = fields.One2many('stable.competition.result', 'search_id', string="Résultats")
    competition_count = fields.Integer("Nombre de compétitions", compute='_compute_competition_count')
    
    # Paramètres automatiques
    auto_search = fields.Boolean("Recherche automatique", default=False, 
                                help="Effectue une recherche automatique chaque semaine")
    last_auto_search = fields.Datetime("Dernière recherche auto")
    notification_emails = fields.Text("Emails de notification", 
                                     help="Emails séparés par des virgules pour recevoir les nouvelles compétitions")
    
    # Statut
    search_status = fields.Selection([
        ('draft', 'Brouillon'),
        ('searching', 'Recherche en cours'),
        ('completed', 'Terminé'),
        ('error', 'Erreur'),
    ], string="Statut", default='draft', tracking=True)
    
    error_message = fields.Text("Message d'erreur")

    @api.depends('competition_ids')
    def _compute_competition_count(self):
        for record in self:
            record.competition_count = len(record.competition_ids)
    
    def action_view_results(self):
        """Ouvre la vue des résultats de cette recherche"""
        return {
            'name': f'Résultats: {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'stable.competition.result',
            'view_mode': 'list,form',
            'domain': [('search_id', '=', self.id)],
            'context': {'search_default_upcoming': 1}
        }

    def action_search_competitions(self):
        """Lance la recherche de compétitions"""
        self.search_status = 'searching'
        self.error_message = False
        
        try:
            # Supprimer les anciens résultats
            self.competition_ids.unlink()
            
            # Effectuer la recherche
            competitions = self._scrape_ffe_competitions()
            
            # Créer les résultats
            for comp_data in competitions:
                self.env['stable.competition.result'].create({
                    'search_id': self.id,
                    'name': comp_data.get('name', 'Compétition sans nom'),
                    'location': comp_data.get('location', ''),
                    'date_start': comp_data.get('date_start'),
                    'date_end': comp_data.get('date_end'),
                    'discipline': comp_data.get('discipline', self.discipline),
                    'level': comp_data.get('level', ''),
                    'organizer': comp_data.get('organizer', ''),
                    'url': comp_data.get('url', ''),
                    'description': comp_data.get('description', ''),
                    'entry_deadline': comp_data.get('entry_deadline'),
                    'contact_info': comp_data.get('contact_info', ''),
                })
            
            self.search_status = 'completed'
            self.search_date = fields.Datetime.now()
            
            # Poster un message dans le chatter
            self.message_post(
                body=f"Recherche terminée : {len(competitions)} compétitions trouvées",
                subject="Recherche de compétitions FFE"
            )
            
        except Exception as e:
            _logger.error(f"Erreur lors de la recherche FFE: {str(e)}")
            self.search_status = 'error'
            self.error_message = str(e)
            
    def _scrape_ffe_competitions(self):
        """Scrape les compétitions depuis FFEcompet (simulation)"""
        # Note: En l'absence d'API officielle, voici une approche de web scraping
        # ATTENTION: Le web scraping doit respecter les conditions d'utilisation du site
        
        competitions = []
        
        try:
            # Simuler des données pour démonstration
            # Dans un vrai environnement, vous devriez utiliser des techniques de web scraping
            sample_competitions = [
                {
                    'name': 'Concours de CSO - Nord Équestre',
                    'location': 'Lille (59)',
                    'date_start': '2025-02-15',
                    'date_end': '2025-02-16', 
                    'discipline': 'cso',
                    'level': 'amateur',
                    'organizer': 'Nord Équestre',
                    'url': 'https://ffecompet.ffe.com/concours/exemple',
                    'description': 'Concours de saut d\'obstacles amateur',
                    'entry_deadline': '2025-02-10',
                    'contact_info': 'contact@nordequestre.fr'
                },
                {
                    'name': 'Championnat Régional CSO Normandie',
                    'location': 'Caen (14)',
                    'date_start': '2025-03-01',
                    'date_end': '2025-03-03',
                    'discipline': 'cso', 
                    'level': 'pro',
                    'organizer': 'Comité Régional Normandie',
                    'url': 'https://ffecompet.ffe.com/concours/exemple2',
                    'description': 'Championnat régional de saut d\'obstacles',
                    'entry_deadline': '2025-02-25',
                    'contact_info': 'normandie@ffe.com'
                },
                {
                    'name': 'CSO Club Île-de-France',
                    'location': 'Fontainebleau (77)',
                    'date_start': '2025-02-22',
                    'date_end': '2025-02-23',
                    'discipline': 'cso',
                    'level': 'club',
                    'organizer': 'Centre Équestre de Fontainebleau',
                    'url': 'https://ffecompet.ffe.com/concours/exemple3',
                    'description': 'Concours club de saut d\'obstacles',
                    'entry_deadline': '2025-02-18',
                    'contact_info': 'fontainebleau@equipedia.fr'
                }
            ]
            
            # Filtrer selon les critères de recherche
            for comp in sample_competitions:
                if self._matches_search_criteria(comp):
                    competitions.append(comp)
                    
        except Exception as e:
            _logger.error(f"Erreur scraping FFE: {str(e)}")
            raise
            
        return competitions
    
    def _matches_search_criteria(self, competition):
        """Vérifie si une compétition correspond aux critères de recherche"""
        # Vérifier la discipline
        if self.discipline and competition.get('discipline') != self.discipline:
            return False
            
        # Vérifier le niveau
        if self.level and competition.get('level') != self.level:
            return False
            
        # Vérifier la région (logique simplifiée pour la démo)
        if self.region:
            location = competition.get('location', '').lower()
            region_keywords = {
                'hauts-de-france': ['lille', 'valenciennes', 'amiens', 'arras', '59', '62', '02', '60', '80'],
                'normandie': ['caen', 'rouen', 'cherbourg', '14', '27', '50', '61', '76'],
                'ile-de-france': ['paris', 'fontainebleau', 'versailles', '75', '77', '78', '91', '92', '93', '94', '95'],
            }
            
            keywords = region_keywords.get(self.region, [])
            if not any(keyword in location for keyword in keywords):
                return False
                
        # Vérifier les dates
        if self.date_from or self.date_to:
            comp_date = competition.get('date_start')
            if comp_date:
                try:
                    comp_date_obj = datetime.strptime(comp_date, '%Y-%m-%d').date()
                    if self.date_from and comp_date_obj < self.date_from:
                        return False
                    if self.date_to and comp_date_obj > self.date_to:
                        return False
                except:
                    pass
                    
        return True
    
    @api.model  
    def run_auto_searches(self):
        """Méthode appelée par cron pour les recherches automatiques"""
        searches = self.search([
            ('auto_search', '=', True),
            '|',
            ('last_auto_search', '=', False),
            ('last_auto_search', '<=', fields.Datetime.now() - timedelta(days=7))
        ])
        
        for search in searches:
            try:
                search.action_search_competitions()
                search.last_auto_search = fields.Datetime.now()
                
                # Envoyer notifications si nouvelles compétitions
                if search.notification_emails and search.competition_count > 0:
                    search._send_notification_emails()
                    
            except Exception as e:
                _logger.error(f"Erreur recherche auto {search.name}: {str(e)}")
                
    def _send_notification_emails(self):
        """Envoie des emails de notification pour les nouvelles compétitions"""
        if not self.notification_emails:
            return
            
        emails = [email.strip() for email in self.notification_emails.split(',')]
        
        # Template d'email simple
        subject = f"Nouvelles compétitions {self.discipline.upper()} trouvées"
        
        body = f"""
        <h3>Recherche: {self.name}</h3>
        <p>{self.competition_count} compétitions trouvées correspondant à vos critères:</p>
        <ul>
        """
        
        for comp in self.competition_ids[:5]:  # Limiter à 5 pour l'email
            body += f"<li><strong>{comp.name}</strong> - {comp.location} - {comp.date_start}</li>"
            
        body += "</ul>"
        
        if self.competition_count > 5:
            body += f"<p>... et {self.competition_count - 5} autres compétitions</p>"
            
        body += "<p>Consultez Odoo pour voir tous les détails.</p>"
        
        for email in emails:
            try:
                mail_values = {
                    'subject': subject,
                    'body_html': body,
                    'email_to': email,
                    'email_from': self.env.user.email or 'noreply@stable-manager.com',
                }
                mail = self.env['mail.mail'].create(mail_values)
                mail.send()
            except Exception as e:
                _logger.error(f"Erreur envoi email à {email}: {str(e)}")


class StableCompetitionResult(models.Model):
    _name = 'stable.competition.result'
    _description = 'Competition Search Result'
    _order = 'date_start asc'

    search_id = fields.Many2one('stable.competition.search', string="Recherche", ondelete='cascade')
    
    # Informations de base
    name = fields.Char("Nom de la compétition", required=True)
    location = fields.Char("Lieu")
    date_start = fields.Date("Date de début")
    date_end = fields.Date("Date de fin")
    
    # Détails
    discipline = fields.Selection([
        ('cso', 'CSO/Obstacle'),
        ('dressage', 'Dressage'),
        ('complet', 'Complet'),
        ('endurance', 'Endurance'),
        ('attelage', 'Attelage'),
    ], string="Discipline")
    
    level = fields.Char("Niveau")
    organizer = fields.Char("Organisateur")
    url = fields.Char("URL FFEcompet")
    description = fields.Text("Description")
    entry_deadline = fields.Date("Date limite d'engagement")
    contact_info = fields.Char("Contact")
    
    # Actions
    interested = fields.Boolean("Intéressé", default=False)
    notes = fields.Text("Notes")
    
    def action_open_ffe_url(self):
        """Ouvre l'URL FFEcompet dans un nouvel onglet"""
        if self.url:
            return {
                'type': 'ir.actions.act_url',
                'url': self.url,
                'target': 'new'
            }
            
    def action_mark_interested(self):
        """Marque la compétition comme intéressante"""
        self.interested = not self.interested
        
    def action_create_competition_entry(self):
        """Crée une entrée de compétition dans stable.competition"""
        return {
            'name': 'Nouvelle compétition',
            'type': 'ir.actions.act_window',
            'res_model': 'stable.competition',
            'view_mode': 'form',
            'context': {
                'default_location': self.location,
                'default_date': self.date_start,
                'default_discipline': self.discipline,
                'default_more_info': f"Compétition trouvée via recherche FFE: {self.name}\n"
                                   f"Organisateur: {self.organizer}\n"
                                   f"Contact: {self.contact_info}\n"
                                   f"URL: {self.url}"
            }
        }