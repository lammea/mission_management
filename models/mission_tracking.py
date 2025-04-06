from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class MissionTracking(models.Model):
    _name = 'mission.tracking'
    _description = 'Suivi des missions'

    state = fields.Selection([
        ('new', 'Nouvelles'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminée'),
        ('cancelled', 'Annulée')
    ], default='new', string="État", track_visibility='onchange')

    mission_request_id = fields.Many2one('mission.request', string="Demande de mission", required=True)
    mission_number = fields.Char(string="Numéro de mission", readonly=True, copy=False)
    date_start = fields.Date(string="Date de début")
    date_end = fields.Date(string="Date de fin")
    additional_fees = fields.Float(string="Frais supplémentaires")
    overtime_hours = fields.Float(string="Heures supplémentaires")
    total_fees = fields.Float(string="Total des frais", compute="_compute_total_fees", store=True)

    @api.depends('additional_fees', 'overtime_hours')
    def _compute_total_fees(self):
        for record in self:
            record.total_fees = record.additional_fees + (
                        record.overtime_hours * 20)  # Par exemple 20€ par heure supplémentaire

    @api.model
    def create(self, vals):
        # Attribuer automatiquement un numéro séquentiel
        if not vals.get('mission_number'):
            vals['mission_number'] = self.env['ir.sequence'].next_by_code('mission.tracking.sequence')
        return super(MissionTracking, self).create(vals)

    def action_complete(self):
        self.write({'state': 'completed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def _get_report_values(self, docids, data=None):
        # Récupérer l'action du rapport
        report = self.env['ir.actions.report']._get_report_from_name('mission_management.report_mission')

        # Récupérer les enregistrements associés aux docids
        docs = self.env[report.model].browse(docids)

        # Assurez-vous que `docs` contient les enregistrements attendus
        if not docs:
            raise ValueError("Les enregistrements sont introuvables pour les docids spécifiés.")

        # Vérification du contenu de docs (optionnel pour débogage)
        _logger = logging.getLogger(__name__)
        _logger.info("Enregistrements trouvés pour docids: %s", docs)

        return {
            'doc': docs,  # Assurez-vous que 'doc' contient les bons enregistrements
            'data': data,  # Si vous avez d'autres données à passer, vous pouvez les inclure
        }



