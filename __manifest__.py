{
    'name': 'Stable Manager',
    'version': '1.0',
    'summary': 'Gérez vos chevaux, rations, compétitions et stocks de nourriture',
    'description': """
        Module de gestion équestre complet.
        Ce module permet de suivre les informations essentielles d'une écurie :
        - Fiches chevaux (âge, race, etc.)
        - Rations alimentaires journalières
        - Stocks de nourriture
        - Suivi des compétitions (résultats, émotions, performance)

        Destiné aux clubs équestres, cavaliers ou gestionnaires d’écuries.
    """,
    'author': 'Alessandro Pollice',
    'website': 'www.lesecuriesdelm.be',
    'category': 'Equestrian',
    'version': '1.0',
    'depends': ['base', 'mail', 'stock', 'mrp'],

    'data': [
        'data/vaccine_data.xml',
        'data/competition_data.xml',
        'data/horses_data.xml',
        'data/dentist_data.xml',
        'security/ir.model.access.csv',

        'views/reports/horse_report.xml',
        'reports/report.xml',

        'views/horse_views.xml',
        'views/competition_views.xml',
        'views/health_views.xml',
        'views/stable_view_vaccins.xml',
        'views/stable_view_osteopath.xml',
        'views/stable_view_dentist.xml',
        'views/stable_view_farrier.xml',
        'views/stable_view_veterinary.xml',

    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': -2000
}
