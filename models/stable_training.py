from odoo import models, fields, api

class StableTraining(models.Model):
    _name = 'stable.training'
    _description = 'Horses training sessions'

    horse_id = fields.Many2one('stable.horse', string="Horse", required=True, tracking=True)
    start_date = fields.Datetime("Start Date", required=True, tracking=True)
    end_date = fields.Datetime("End Date", required=True, tracking=True)
    progress = fields.Float("Progress (%)", default=0.0, tracking=True)
    assigned_to = fields.Many2one('res.users', string="Assigned To", required=True, tracking=True)
    color= fields.Integer("Color", default=0, tracking=True)