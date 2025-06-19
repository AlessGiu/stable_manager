from odoo import models, fields


class StableFarrier(models.Model):
    _name = 'stable.farrier'
    _description = "Farrier Visit"

    # Link to the horse receiving farrier care
    horse_id = fields.Many2one('stable.horse',
                               string="Horse",
                               required=True)

    # Farrier's identity and contact details
    farrier_name = fields.Char("Farrier Name", required=True)
    farrier_contact = fields.Char("Farrier Contact")

    # Visit details and findings
    reason = fields.Text("Reason for Visit")
    findings = fields.Text("Farrier's Findings")
    work_done = fields.Text("Work Performed")
    recommendations = fields.Text("Recommendations / Follow-up Care")

    # Assessment of hoof health
    hoof_condition = fields.Selection([
        ("excellent", "Excellent"),
        ("bon", "Good"),
        ("limite", "Borderline"),
        ("problemes", "Hoof Problems"),
        ("suivi", "Requires Follow-up")
    ], string="Observed Hoof Condition")

    # Type of farrier intervention performed
    shoe_type = fields.Selection([
        ("ferrage", "Full Shoeing"),
        ("deferrage", "Unshoeing"),
        ("parage", "Trimming Only"),
        ("orthopedique", "Orthopedic Shoeing"),
        ("therapeutique", "Therapeutic Shoeing"),
        ("autres", "Other Interventions")
    ], string="Type of Intervention")

    # Visit scheduling and documentation
    visit_date = fields.Date("Visit Date", default=fields.Date.today)
    next_visit = fields.Date("Recommended Next Visit")

    report = fields.Binary("Farrier Report")
    report_filename = fields.Char("File Name")

    # Materials and shoe size used during the visit
    materials_used = fields.Text("Materials Used")
    shoe_size = fields.Char("Shoe Size")

    # Additional notes for follow-up or context
    notes = fields.Text("Additional Notes")
