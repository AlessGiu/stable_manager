{
    'name': 'Stable Manager',
    'version': '1.0',
    'summary': 'Manage your horses, rations, competitions and feed inventory',
    'description': """
Complete equestrian management module for horse clubs and stables.

This module helps to manage essential operations in a stable:
- Horse records (age, breed, sex, etc.)
- Daily feeding plans and rations
- Feed inventory and stock control
- Competition tracking (results, emotions, performance review)
- Veterinary and health records

Designed for equestrian centers, riders and stable managers.
    """,
    'author': 'Alessandro Pollice',
    'website': 'https://www.lesecuriesdelm.be',  # change if needed
    'category': 'Industry',
    'depends': ['base', 'mail', 'stock', 'mrp', 'sale'],
    'data': [
        'security/res_group.xml',
        'security/ir.model.access.csv',

        'data/horses_data.xml',
        'data/vaccine_data.xml',
        'data/competition_data.xml',
        'data/dentist_data.xml',

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
        # 'views/stable_view_training.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': -2000
}
