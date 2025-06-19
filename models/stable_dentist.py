from odoo import models, fields


class StableDentist(models.Model):
    _name = 'stable.dentist'
    _description = "Equine Dentist Visit"

    # Link to the horse receiving dental care
    horse_id = fields.Many2one('stable.horse', string="Horse", required=True)

    # Dentist's identity and contact details
    dentist_name = fields.Char("Dentist Name", required=True)
    dentist_contact = fields.Char("Dentist Contact")

    # Visit details and findings
    reason = fields.Text("Visit Reason")
    findings = fields.Text("Dentist Findings")
    treatment_done = fields.Text("Dental Treatment Performed")
    recommendations = fields.Text("Recommendations / Follow-up Care")

    # Assessment of dental health
    teeth_condition = fields.Selection([
        ("excellent", "Excellent"),
        ("bon", "Good"),
        ("limite", "Borderline"),
        ("problemes", "Dental Issues"),
        ("suivi", "Requires Follow-up")
    ], string="Observed Dental Condition")

    # Specific dental issues identified
    specific_issues = fields.Selection([
        ("none", "None"),
        ("points", "Sharp Points"),
        ("carie", "Cavities"),
        ("fracture", "Dental Fracture"),
        ("parodonte", "Periodontal Issue"),
        ("autres", "Other Issues")
    ], string="Specific Issues")

    # Visit scheduling and documentation
    visit_date = fields.Date("Visit Date", default=fields.Date.today)
    next_visit = fields.Date("Recommended Next Visit")
    report = fields.Binary("Dental Report")
    report_filename = fields.Char("File Name")

    # Sedation information
    sedation_used = fields.Boolean("Sedation Used")
    sedation_details = fields.Text("Sedation Details")

    # Additional notes for follow-up or context
    notes = fields.Text("Additional Notes")
