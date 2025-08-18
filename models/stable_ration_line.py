from odoo import models, fields


class StableRationLine(models.Model):
    _name = 'stable.ration.line'
    _description = 'Ligne de ration (aliment)'
    _inherit = ['mail.thread', 'mail.activity.mixin']


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

    note = fields.Text(string="Note")

    def open_ration_line_form(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stable.ration.line',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',  # modal
        }

