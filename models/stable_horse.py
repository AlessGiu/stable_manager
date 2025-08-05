from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class StableHorses(models.Model):
    _name = 'stable.horse'
    _description = 'Horse'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Enables communication and activity tracking

    # === Identity ===
    name = fields.Char("Horse Name", required=True)
    owner_id = fields.Many2one('res.partner', string="Owner", tracking=True)
    sireno = fields.Char("SIRE Number")
    sexe = fields.Selection([
        ("hongre", "Gelding"),
        ("etalon", "Stallion"),
        ("jument", "Mare")
    ], string="Sex")

    birth_date = fields.Date("Birth Date")
    age = fields.Integer("Age", compute='_compute_age', store=True)

    # === Physical Characteristics ===
    robe = fields.Selection([
        ("alezan", "Chestnut"),
        ("bai", "Bay"),
        ("bai_brule", "Burnt Bay"),
        ("bai_clair", "Light Bay"),
        ("bai_fonce", "Dark Bay"),
        ("noir", "Black"),
        ("gris", "Gray"),
        ("isabelle", "Buckskin"),
        ("palomino", "Palomino"),
        ("pie_noir", "Black Pinto"),
        ("pie_bai", "Bay Pinto"),
        ("pie_alezan", "Chestnut Pinto"),
        ("appaloosa", "Appaloosa"),
    ], string="Coat")

    taille = fields.Integer("Height (cm)", required=True)
    poids = fields.Integer("Weight (kg)", required=True)

    puce_elec = fields.Boolean(
        default=True,
        string="Microchipped",
        help="Indicates whether the horse has an electronic chip."
    )

    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)

    # === Boarding & Competition ===
    type_pension = fields.Selection([
        ("classic", "Classic"),
        ("work", "Work"),
        ("consignment", "Consignment"),
        ("breaking", "Breaking"),
        ("personnal", "Personal")
    ], string="Boarding Type", tracking=True, default="classic")

    in_competition = fields.Boolean("In Competition?", default=False, tracking=True)
    competition_this_year = fields.Integer(
        string="Competitions This Year",
        compute='_compute_competition_this_year',
    )

    # === Linked Records ===
    competition_ids = fields.One2many('stable.competition', 'horse_id', string="Competition History")
    vaccins_ids = fields.One2many('stable.vaccins', 'horse_id', string="Vaccination Records", stat_button=False)
    osteopath_ids = fields.One2many('stable.osteopath', 'horse_id', string="Osteopath Visits")
    dentist_ids = fields.One2many('stable.dentist', 'horse_id', string="Dental Records")
    farrier_ids = fields.One2many('stable.farrier', 'horse_id', string="Farrier Records")
    veterinary_ids = fields.One2many('stable.veterinary', 'horse_id', string="Veterinary Records")

    # === Feeding / Rations ===
    ration_id = fields.Many2one('stable.ration', string="Ration")
    ration_line_ids = fields.One2many(
        related='ration_id.ration_line_ids',
        string="Ration Lines"
    )

    # === Computed Fields ===

    @api.depends('birth_date')
    def _compute_age(self):
        """Compute the horse's age from the birth date."""
        today = date.today()
        for record in self:
            if record.birth_date:
                record.age = today.year - record.birth_date.year - (
                        (today.month, today.day) < (record.birth_date.month, record.birth_date.day)
                )
            else:
                record.age = 0

    def _compute_competition_this_year(self):
        """Compute the number of competitions the horse has participated in during the current year."""
        current_year = date.today().year
        start_date = date(current_year, 1, 1)
        today = date.today()
        for horse in self:
            horse.competition_this_year = self.env['stable.competition'].search_count([
                ('horse_id', '=', horse.id),
                ('date', '>=', start_date),
                ('date', '<=', today)
            ])

    # === Constraints ===

    @api.constrains('birth_date')
    def _check_birth_date(self):
        """Ensure the birth date is not in the future."""
        for record in self:
            if record.birth_date and record.birth_date > date.today():
                raise ValidationError("The birth date cannot be in the future.")

    @api.constrains('name')
    def _check_name(self):
        """Validate the horse's name (presence, length, uniqueness)."""
        for record in self:
            if not record.name:
                raise ValidationError("The horse name cannot be empty.")
            if len(record.name) < 3:
                raise ValidationError("The horse name must be at least 3 characters long.")
            if len(record.name) > 50:
                raise ValidationError("The horse name must not exceed 50 characters.")
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError("This horse already exists.")

    @api.constrains('owner_id')
    def _check_owner(self):
        """Ensure the horse has an owner."""
        for record in self:
            if not record.owner_id:
                raise ValidationError("Please select or create an owner for the horse.")

    @api.constrains('taille', 'poids')
    def _check_size_weight(self):
        """Ensure that height and weight are both greater than zero."""
        for rec in self:
            if rec.taille <= 0:
                raise ValidationError("Height must be greater than zero.")
            if rec.poids <= 0:
                raise ValidationError("Weight must be greater than zero.")

    # === Custom Actions ===

    def action_add_ration_line(self):
        """
        Add a new ration line for the horse.

        If no ration is linked to the horse, create one along with a product.template.
        Then open the ration line form with the ration ID pre-filled.

        Returns:
            dict: Odoo action to open a modal form for stable.ration.line
        """
        self.ensure_one()

        if not self.ration_id:
            product_template = self.env['product.template'].create({
                'name': f"Ration - {self.name}",
                'type': 'consu',
            })

            ration = self.env['stable.ration'].create({
                'product_tmpl_id': product_template.id,
            })

            self.ration_id = ration

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stable.ration.line',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_ration_id': self.ration_id.id,
            }
        }
