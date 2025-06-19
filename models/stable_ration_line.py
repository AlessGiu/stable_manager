from odoo import models, fields


class StableRationLine(models.Model):
    _name = "stable.ration.line"
    _description = "Élément de ration"

    ration_id = fields.Many2one('stable.ration', string="Ration")
    ingredient = fields.Char("Ingrédient")  # ou relation à un modèle stable.ingredient si tu veux
    quantity = fields.Float("Quantité")
