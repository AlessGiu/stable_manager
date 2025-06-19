# Odoo model for managing competition tags assigned to horses
from odoo import models, fields


class StableHorseTag(models.Model):
    _name = 'stable.horse.tag'
    _description = 'Competition Tag'

    # Name of the tag (e.g., "Show Jumping", "Dressage")
    name = fields.Char("Tag Name",
                       required=True,
                       help="Name of the competition tag")

    # Indicates if the tag is currently active and usable
    active = fields.Boolean("Active",
                            default=True,
                            help="Indicates if the tag is currently active")

    # Color code for easy visual identification in the interface
    color = fields.Integer("Color")
