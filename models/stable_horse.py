from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class StableHorses(models.Model):
    _name = 'stable.horse'
    _description = 'Horse'
    _inherit = 'mail.thread', 'mail.activity.mixin'  # Enables communication and activity tracking

    # Main identity fields for each horse
    name = fields.Char("Horse Name", required=True)
    owner_id = fields.Many2one('res.partner', string="Owner", tracking=True)  # Owner of the horse
    sireno = fields.Char("SIRE Number")
    sexe = fields.Selection([
        ("hongre", "Gelding"),
        ("etalon", "Stallion"),
        ("jument", "Mare")])

    birth_date = fields.Date("Birth Date")
    age = fields.Integer("Age", compute='_compute_age', store=True)  # Automatically calculated from birth date

    # Physical characteristics
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

    type_pension = fields.Selection([
        ("classic", "Classic"),
        ("work", "Work"),
        ("consignment", "Consignment"),
        ("breaking", "Breaking"),
        ("personnal", "Personal")
    ], tracking=True, default="classic", string="Pension Type")  # Type of boarding

    taille = fields.Integer("Height (cm)", required=True)
    race = fields.Selection([
        ("selle_francais", "Selle Français"),
        ("lusitano", "Lusitano"),
        ("kwpn", "KWPN"),
        ("hanoverian", "Hanoverian"),
        ("trakehner", "Trakehner"),
        ("holsteiner", "Holsteiner"),
        ("irish_sport_horse", "Irish Sport Horse"),
        ("oldenburg", "Oldenburg"),
        ("andalusian", "Andalusian"),
        ("arabian", "Arabian"),
        ("friesian", "Friesian"),
        ("paint", "Paint Horse"),
        ("quarter", "Quarter Horse"),
        ("connemara", "Connemara"),
        ("haflinger", "Haflinger"),
        ("pony", "Pony"),
        ("thoroughbred", "Thoroughbred"),
        ("warmblood", "Warmblood"),
    ], string="Breed")

    poids = fields.Integer("Weight (kg)", required=True)
    puce_elec = fields.Boolean(
        default=True,
        string="Microchipped",
        help="Indicates whether the horse has an electronic chip."
    )

    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)  # Horse photo

    in_competition = fields.Boolean("In Competition?", default=False, tracking=True)  # Competition status
    competition_this_year = fields.Integer(
        string="Competitions This Year",
        compute='_compute_competition_this_year',
    )

    # Linked records for health, feeding, and competitions
    competition_ids = fields.One2many('stable.competition', 'horse_id', string="Competition History")
    vaccins_ids = fields.One2many('stable.vaccins', 'horse_id', string="Vaccination Records")
    osteopath_ids = fields.One2many('stable.osteopath', 'horse_id', string="Osteopath Visits")
    dentist_ids = fields.One2many('stable.dentist', 'horse_id', string="Dental Records")
    farrier_ids = fields.One2many('stable.farrier', 'horse_id', string="Farrier Records")
    veterinary_ids = fields.One2many('stable.veterinary', 'horse_id', string="Veterinary Records")

    ration_mrp_ids = fields.Many2many(
        'mrp.production',
        string="Rations MRP"
    )

    # Automatically computes the age based on the birth date
    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.birth_date:
                record.age = today.year - record.birth_date.year - (
                        (today.month, today.day) < (record.birth_date.month, record.birth_date.day)
                )
            else:
                record.age = 0

    # Automatically computes the number of competitions this year
    def _compute_competition_this_year(self):
        current_year = date.today().year
        start_date = date(current_year, 1, 1)
        today = date.today()
        for horse in self:
            horse.competition_this_year = self.env['stable.competition'].search_count([
                ('horse_id', '=', horse.id),
                ('date', '>=', start_date),
                ('date', '<=', today)
            ])

    @api.constrains('birth_date')
    def _check_birth_date(self):
        for record in self:
            if record.birth_date and record.birth_date > date.today():
                raise ValidationError("The birth date cannot be in the future.")

    @api.constrains('name')
    def _check_name(self):
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
        for record in self:
            if not record.owner_id:
                raise ValidationError("Please select/create an owner for the horse.")
