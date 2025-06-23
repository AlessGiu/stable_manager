from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    horse_ids = fields.Many2many(
        'stable.horse',
        string="Chevaux"
    )

    # IS RATION ?
    # DOMAIN POUR FILTRER LES RATIONS