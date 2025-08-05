from odoo import models, fields, api


class StableRation(models.Model):
    _name = 'stable.ration'
    _inherits = {'product.template': 'product_tmpl_id'}
    _description = 'Ration alimentaire pour cheval'

    product_tmpl_id = fields.Many2one(
        'product.template',
        required=True,
        ondelete='cascade',
        string='Produit de référence'
    )

    horse_ids = fields.One2many(
        'stable.horse',
        'ration_id',
        string='Horses',
        required=True
    )

    preparation_note = fields.Text(string="Remarques / Préparation")
    is_ration = fields.Boolean(string="Est une ration ?", default=True)

    ration_line_ids = fields.One2many(
        'stable.ration.line',
        'ration_id',
        string='Lignes d’aliments'
    )
