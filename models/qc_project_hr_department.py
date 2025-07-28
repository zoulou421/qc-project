# -*- coding: utf-8 -*-
from odoo import models, fields


class QCProjectHRDepartment(models.Model):
    _inherit = 'hr.department'

    dpt_type = fields.Selection([('internal', 'Internal'), ('external', 'External')], string="Department Type",
                                index=True)
  #domain_id // many2one