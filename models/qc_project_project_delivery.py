# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QCProjectProjectDelivery(models.Model):
    _name = 'qcproject.projectdelivery'
    _description = 'A Project_Delivery is validated by a Manager'

    project_id = fields.Many2one('qcproject.project', string='Project')
    employee_id = fields.Many2one('qcproject.employee', string='Project Manager')
    on_time = fields.Boolean(string='On Time')
    comments = fields.Text(string='Comments')
    delivery_date = fields.Date(string='Delivery Date')
