# Odoo model for tracking osteopath visits and treatments for horses
from odoo import models, fields


class StableOsteopath(models.Model):
    _name = 'stable.osteopath'
    _description = "Osteopath Visit"

    # Link to the horse receiving osteopathic care
    horse_id = fields.Many2one('stable.horse', string="Horse", required=True)

    # Osteopath's identity and contact details
    osteopath_name = fields.Char("Osteopath Name", required=True)
    osteopath_contact = fields.Char("Osteopath Contact")

    # Visit details and findings
    reason = fields.Text("Reason for Visit")
    findings = fields.Text("Osteopath's Findings")
    treatment_done = fields.Text("Treatment Performed")
    recommendations = fields.Text("Recommendations / Follow-up Care")

    # Assessment of the horse's general condition
    general_condition = fields.Selection([
        ("excellent", "Excellent"),
        ("bon", "Good"),
        ("raideur", "Stiffness"),
        ("douleur", "Pain / Blockage"),
        ("suivi", "Requires Follow-up")
    ], string="Observed General Condition")

    # Visit scheduling and documentation
    visit_date = fields.Date("Visit Date", default=fields.Date.today)
    next_visit = fields.Date("Recommended Next Visit")
    report = fields.Binary("Osteopathic Report")
    report_filename = fields.Char("File Name")

    # Additional notes for follow-up or context
    notes = fields.Text("Additional Notes")
