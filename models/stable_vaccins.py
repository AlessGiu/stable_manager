from odoo import models, fields, api


class StableHealth(models.Model):
    _name = 'stable.vaccins'
    _description = 'Horse Vaccines'

    horse_id = fields.Many2one('stable.horse', string="Horse")
    vet_name = fields.Char(string="Veterinarian Name")
    vet_contact = fields.Char(string="Veterinarian Contact")
    vet_clinic = fields.Char(string="Veterinarian Clinic")
    medical_history = fields.Char(string="Medical History")

    vaccine_type = fields.Selection([
        ('tetanos', 'Tetanus'),
        ('grippe', 'Equine Influenza'),
        ('rage', 'Rabies'),
        ('rhinopneumonie', 'Rhinopneumonitis'),
        ('autre', 'Other')
    ], string="Vaccine Type")

    global_health = fields.Selection([
        ("excellent", "Excellent"),
        ("bon", "Good"),
        ("a surveiller", "To Monitor"),
        ("convalescent", "Convalescent")
    ], string="Overall Health")

    report = fields.Binary(string="Veterinary Report")
    report_filename = fields.Char(string="File Name")
    date_vaccine = fields.Date(string="Vaccination Date")

    next_reminder = fields.Date(
        string="Next Vaccine/Worming",
        compute='_compute_next_vermifuge',
        store=True,
        readonly=False
    )
    notes = fields.Text(string="Observations")

    @api.depends('date_vaccine')
    def _compute_next_vermifuge(self):
        for record in self:
            record.next_reminder = (fields.Date.add
                                    (record.date_vaccine,
                                     months=6)
                                    ) if record.date_vaccine \
                else False
