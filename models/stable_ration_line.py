from odoo import models, fields


class StableRationLine(models.Model):
    _name = 'stable.ration.line'
    _description = 'Ligne de ration (aliment)'

    quantity = fields.Float(string="Quantity", required=True)

    ration_id = fields.Many2one('stable.ration',
                                string="Ration",
                                required=True)

    product_id = fields.Many2one('product.product',
                                 string="Food",
                                 required=True)

    uom_id = fields.Many2one('uom.uom',
                             string="Unit",
                             required=True)

    note= fields.Text(string="Note")
