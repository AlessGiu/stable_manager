# Odoo model for managing and tracking horse feed rations
from odoo import models, fields


class StableRation(models.Model):
    _name = 'stable.ration'
    _description = 'Feed Ration'
    _inherit = ['mail.thread']

    # Name of the ration, computed for easy identification
    name = fields.Char(string="Ration Name", compute='_compute_name')

    # Indicates if the ration is currently active
    active = fields.Boolean(string="Active", default=True)

    # Additional notes for context or follow-up
    notes = fields.Text(string="Additional Notes")

    # Type of grain given in the morning
    morning_grain_type = fields.Selection([
        ('none', 'None'),
        ('classic', 'Classic Grains'),
        ('care4life', 'Care4Life'),
        ('specific_energy', 'Reverdy Specific Energy'),
        ('perry', 'Perry Grains'),
        ('zoe', 'Zoé Grains'),
        ('daphne', 'Daphné Grains'),
        ('big_grains', 'Large Pellet Grains'),
        ('other', 'Other (specify)'),
    ], string="Morning Grain Type", default='none')

    # Quantity of feed given
    quantity = fields.Selection([
        ('qty', '1 scoop'),
        ('qty2', '1 measure'),
        ('qty3', '1 handful'),
    ], string="Quantity", required=True)

    # Link to the horse receiving this ration
    horse_id = fields.Many2one('stable.horse', string="Horse", required=True)

    # Time of day the ration is given (morning/evening)
    moment = fields.Selection([
        ('morning', 'Morning'),
        ('evening', 'Evening')
    ], string="Time of Day", required=True)

    # List of detailed ration components (e.g., hay, supplements)
    ration_line_ids = fields.One2many('stable.ration.line', 'ration_id', string="Ration Contents")

    # Log a message when the ration is modified
    def write(self, vals):
        res = super().write(vals)
        self.message_post(body="⚠️ Ration modified.")
        return res
