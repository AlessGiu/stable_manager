from odoo import models, fields, api


class StableVeterinary(models.Model):
    _name = 'stable.veterinary'
    _description = "Global Veterinary Visit"

    horse_id = fields.Many2one('stable.horse', string="Horse", required=True)
    vet_name = fields.Char(string="Veterinarian Name", required=True)
    vet_contact = fields.Char(string="Veterinarian Contact")
    clinic_name = fields.Char(string="Veterinary Clinic")
    clinic_address = fields.Text(string="Clinic Address")

    hospitalization = fields.Boolean(string="Hospitalization Required")
    surgery_required = fields.Boolean(string="Surgery Required")
    surgery_done = fields.Boolean(string="Surgery Completed")
    surgery_date = fields.Date(string="Surgery Date")
    follow_up_required = fields.Boolean(string="Follow-Up Required")

    visit_date = fields.Date(string="Visit Date", default=fields.Date.today)
    next_visit = fields.Date(string="Recommended Next Visit")
    reason = fields.Text(string="Visit Reason", required=True)
    findings = fields.Text(string="Veterinarian Findings")
    diagnosis = fields.Text(string="Diagnosis")
    treatment = fields.Text(string="Prescribed Treatment")
    recommendations = fields.Text(string="Recommendations")

    medication_ids = fields.One2many(
        'stable.veterinary.medication', 'visit_id', string="Prescribed Medications"
    )

    exams_done = fields.Selection([
        ("none", "None"),
        ("blood", "Blood Test"),
        ("xray", "X-Ray"),
        ("ultrasound", "Ultrasound"),
        ("scanner", "CT Scan"),
        ("mri", "MRI"),
        ("other", "Other")
    ], string="Exams Performed")
    other_exams = fields.Text(string="Other Specified Exams")
    exam_results = fields.Binary(string="Exam Results")
    exam_filename = fields.Char(string="File Name")

    report = fields.Binary(string="Veterinary Report")
    report_filename = fields.Char(string="Report File Name")
    invoice = fields.Binary(string="Invoice")
    invoice_filename = fields.Char(string="Invoice File Name")

    cost = fields.Float(string="Visit Cost (€)")
    insurance_covered = fields.Boolean(string="Covered by Insurance")
    notes = fields.Text(string="Additional Notes")

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record.horse_id:
            record.horse_id.message_post(
                body=f"New medication prescribed for {record.horse_id.name} "
                     f"on {record.visit_date}. Medication: {record. medication_ids or 'N/A'}. "
            )
        return record


class StableVeterinaryMedication(models.Model):
    _name = 'stable.veterinary.medication'
    _description = "Medications Prescribed During a Veterinary Visit"

    visit_id = fields.Many2one('stable.veterinary', string="Veterinary Visit")
    medication = fields.Char(string="Medication", required=True)
    dosage = fields.Char(string="Dosage")
    duration = fields.Char(string="Treatment Duration")
    purpose = fields.Char(string="Treatment Purpose")
    notes = fields.Text(string="Notes")
