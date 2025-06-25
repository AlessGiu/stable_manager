from odoo import models, fields, api


class StableCompetition(models.Model):
    _name = 'stable.competition'
    _description = 'Equestrian Competition'

    # Date and location of the competition
    date = fields.Date("Date", required=True)
    location = fields.Char("Location")

    # Competition level (e.g., Club, Amateur, Pro, International)
    level = fields.Selection([
        ('club', 'Club'),
        ('amateur', 'Amateur'),
        ('pro', 'Pro'),
        ('international', 'International'),
    ], default='amateur', string="Level")

    # Discipline of the competition (e.g., CSO, Dressage, Eventing)
    discipline = fields.Selection([
        ('csodressage', 'CSO Dressage'),
        ('cso', 'CSO'),
        ('dressage', 'Dressage'),
        ('complet', 'Eventing'),
        ('endurance', 'Endurance'),
        ('attelage', 'Driving'),
    ], required=True, string="Discipline")

    # Result and ranking information
    result = fields.Selection([
        ('sf', 'Clear round'),
        ('4pts', '4 points'),
        ('8pts', '8 points'),
        ('more', 'More'),
        ('eliminated', 'Eliminated'),
        ('dns', 'Did not start'),
    ], string="Result")
    ranking = fields.Integer("Ranking")
    penalty_points = fields.Float("Penalty points", help="Total penalty points")
    prize_money = fields.Float("Prize won (€)")
    time = fields.Float("Time (s)", help="Time achieved if relevant")

    # Rider's emotion and performance analysis
    emotion = fields.Selection([
        ('happy', 'Happy'),
        ('nervous', 'Nervous'),
        ('tired', 'Tired'),
        ('motivated', 'Motivated'),
        ('frustrated', 'Frustrated'),
    ], string="Emotion felt")
    performance_review = fields.Text("Performance analysis")
    improvements = fields.Text("Points to improve", help="Aspects to work on")
    more_info = fields.Text("Additional information")

    # Attachments for competition photos or documents
    attachment_ids = fields.Many2many('ir.attachment', string="Competition photos")

    # Link to the horse that participated in the competition
    horse_id = fields.Many2one('stable.horse', string="Horse", required=True)


    # chatter message when a new competition is created
    @api.model
    def create(self, vals):
        competition = super().create(vals)

        if competition.horse_id:
            competition.horse_id.message_post(
                body=f"New competition added: {competition.location} on {competition.date}. Result: {competition.result or 'N/A'}",)
        return competition
