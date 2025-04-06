
from odoo import models, fields, api

class MissionTrackingReport(models.AbstractModel):
    _name = 'report.mission_management.report_mission'
    _description = 'Rapport de Bon de Mission'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['mission.tracking'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'mission.tracking',
            'docs': docs,
            'total_fees': sum(doc.total_fees for doc in docs)
        }
