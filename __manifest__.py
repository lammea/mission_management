{
    'name': "Gestion des Missions",
    'version': '1.0',
    'depends': ['base', "hr"],
    'author': "Lamia",
    'category': 'Human Resources',
    'description': """Module de gestion des demandes et du suivi des missions.""",

    # data files always loaded at installation
    'data': [
        'views/mission_request_views.xml',
        'views/mission_tracking_views.xml',
        'data/mission_tracking_sequence.xml',
        'views/report_mission_template.xml',  # Ajouter le modèle de rapport

    ],
'assets': {
    'web.report_assets_common': [
        'web/static/src/scss/report.scss',
    ],
},


    'installable': True,
    'application': True,
}
