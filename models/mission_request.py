# models/mission_request.py
from odoo import models, fields, api
from odoo.odoo.exceptions import UserError


class MissionRequest(models.Model):
    _name = 'mission.request'
    _description = 'Demande de mission'

    employee_id = fields.Many2one('hr.employee', string="Employé", required=True)
    department_id = fields.Many2one(related='employee_id.department_id', string="Département", store=True)
    phone = fields.Char(related='employee_id.work_phone', string="Téléphone", store=True)
    email = fields.Char(related='employee_id.work_email', string="Email", store=True)

    vehicle_type = fields.Selection([
        ('personnel', 'Véhicule personnel'),
        ('entreprise', 'Véhicule de l entreprise')
    ], string="Type de véhicule", required=True)

    vehicle_id = fields.Many2one(
        'fleet.vehicle',
        string="Véhicule de l'entreprise",
    )

    mission_reason = fields.Text(string="Motif de la mission", required=True)
    date_start = fields.Date(string="Date de début", required=True)
    date_end = fields.Date(string="Date de fin")

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('accepted', 'Acceptée'),
        ('refused', 'Refusée')
    ], default='draft', string="État", track_visibility='onchange')

    mission_tracking_id = fields.One2many('mission.tracking', 'mission_request_id', string="Suivi des missions")

    def action_approve(self):
        """Action pour approuver la mission"""
        if self.state == 'draft':
            self.write({'state': 'accepted'})
            # Créer un enregistrement de suivi de mission
            mission_tracking = self.env['mission.tracking'].create({
                'mission_request_id': self.id,
                'state': 'new',  # L'état initial du suivi est "Nouvelles"
                'date_start': self.date_start,
                'date_end': self.date_end,
            })
            # Assigner le numéro de mission séquentiel
            mission_tracking.mission_number = self.env['ir.sequence'].next_by_code('mission.tracking.sequence')

    def action_reject(self):
        """Action pour rejeter la mission"""
        if self.state == 'draft':
            self.write({'state': 'refused'})

    def action_delete(self):
        """Action pour supprimer la demande de mission et les missions associées"""
        if self.state == 'draft':
            # Supprimer les enregistrements de suivi des missions associés
            self.mission_tracking_id.unlink()
            # Supprimer la demande de mission elle-même
            self.unlink()
        else:
            raise UserError("Impossible de supprimer une demande de mission qui n'est pas en état 'Brouillon'.")

    @api.onchange('vehicle_type')
    def _onchange_vehicle_type(self):
        """Réinitialiser le véhicule si le type de véhicule n'est pas 'entreprise'"""
        if self.vehicle_type != 'entreprise':
            self.vehicle_id = False
