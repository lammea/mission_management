# mission_management/report/report_mission.py

from odoo import models, api

class ReportMission(models.AbstractModel):
    _name = 'report.mission_management.report_mission'
    _description = 'Rapport PDF Bon de Mission'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['mission.tracking'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'mission.tracking',
            'docs': docs,
        }
