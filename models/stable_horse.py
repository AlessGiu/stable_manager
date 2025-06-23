from odoo import models, fields, api
from datetime import date


class StableHorses(models.Model):
    _name = 'stable.horse'
    _description = 'Horse'
    _inherit = 'mail.thread', 'mail.activity.mixin'  # Enables communication and activity tracking

    # Main identity fields for each horse
    name = fields.Char("Horse Name", required=True)
    sireno = fields.Char("SIRE Number")  # Official French horse registry number
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
    race = fields.Char("Breed")
    poids = fields.Integer("Weight")
    puce_elec = fields.Boolean(
        default=True,
        string="Microchipped",
        help="Indicates whether the horse has an electronic chip."
    )

    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)  # Horse photo

    in_competition = fields.Boolean("In Competition?", default=False, tracking=True)  # Competition status

    # Linked records for health, feeding, and competitions
    competition_ids = fields.One2many('stable.competition', 'horse_id', string="Competition History")
    vaccins_ids = fields.One2many('stable.vaccins', 'horse_id', string="Vaccination Records")
    osteopath_ids = fields.One2many('stable.osteopath', 'horse_id', string="Osteopath Visits")
    dentist_ids = fields.One2many('stable.dentist', 'horse_id', string="Dental Records")
    farrier_ids = fields.One2many('stable.farrier', 'horse_id', string="Farrier Records")
    veterinary_ids = fields.One2many('stable.veterinary', 'horse_id', string="Veterinary Records")

    competition_tags_ids = fields.Many2many(
        'stable.horse.tag',
        string="Competition Tags",
        help="Tags associated with the horse for competition purposes."
    )

    ration_mrp_ids = fields.Many2many(
        'mrp.production',
        string="Rations MRP"
    )

    @api.depends('birth_date')
    def _compute_age(self):
        """Automatically calculates the horse's age based on its birth date."""
        today = date.today()
        for record in self:
            if record.birth_date:
                record.age = today.year - record.birth_date.year - (
                        (today.month, today.day) < (record.birth_date.month, record.birth_date.day)
                )
            else:
                record.age = 0
