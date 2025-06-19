# Odoo model for tracking horse health interventions and medical history
from odoo import models, fields


class StableHealth(models.Model):
    _name = 'stable.health'
    _description = 'Horse Health'

    # Link to the horse concerned by this health record
    horse_id = fields.Many2one('stable.horse', string="Horse")

    # Veterinarian details
    vet_name = fields.Char("Veterinarian Name")
    vet_contact = fields.Char("Veterinarian Contact")
    vet_clinic = fields.Char("Veterinary Clinic")
    medical_history = fields.Char("Medical History")

    # Type of health intervention (e.g., vaccine, dewormer, farrier, dentist)
    type = fields.Selection([
        ('vaccin', 'Vaccine'),
        ('vermifuge', 'Dewormer'),
        ('marechal', 'Farrier'),
        ('dentiste', 'Dentist'),
        ('ostheo', 'Osteopath'),
        ('bilan', 'General Checkup'),
        ('urgence', 'Emergency'),
        ('autre', 'Other')
    ], string="Type of Intervention")

    # Vaccine details (if applicable)
    vaccine_type = fields.Selection([
        ('tetanos', 'Tetanus'),
        ('grippe', 'Equine Influenza'),
        ('rage', 'Rabies'),
        ('rhinopneumonie', 'Rhinopneumonitis'),
        ('autre', 'Other')
    ], string="Vaccine Type")

    # Dewormer details (if applicable)
    dewormer_product = fields.Char("Product Used")
    dewormer_next_date = fields.Date("Next Deworming")

    # Overall health assessment
    global_health = fields.Selection([
        ("excellent", "Excellent"),
        ("bon", "Good"),
        ("a surveiller", "To Monitor"),
        ("convalescent", "Convalescent")],
        string="Overall Health")

    # Attachments for veterinary reports or documents
    report = fields.Binary("Veterinary Report")
    report_filename = fields.Char("File Name")

    # Dates for last and next health checks
    last_examination = fields.Date("Last Examination Date")
    next_reminder = fields.Date("Next Vaccine/Dewormer")

    # Additional notes or observations
    notes = fields.Text(string="Observations")

    # Example for future: compute next vaccine date automatically
    # @api.depends('last_vaccin')
    # def _compute_next_vaccin(self):
    #     pass
