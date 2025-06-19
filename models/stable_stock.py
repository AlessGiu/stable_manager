from odoo import models, fields


class StableStock(models.Model):
    _name = 'stable.stock'
    _description = 'Stock de nourriture'

    name = fields.Char("Nom du produit", required=True)
    type = fields.Selection([
        ('grain', 'Grain'),
        ('fibre', 'Fibre'),
        ('complement', 'Complément'),
    ], string="Type", required=True)
    quantity_available = fields.Float("Quantité disponible (kg)", required=True)
    unit_price = fields.Float("Prix unitaire (€/kg)")
