# -*- coding: utf-8 -*-

from odoo import models, fields, api

class QCProjectSubTask(models.Model):

    _name = 'qcproject.subtask'
    _description = 'A Sub_Task depends on a Task'

    task_id = fields.Many2one('qcproject.task', string='Task')
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    employee_id = fields.Many2one('qcproject.employee', string='Assigned Employee') # Décommenter pour activer l'assignation d'employés
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    status = fields.Selection([('in_progress', 'In Progress'), ('completed', 'Completed')], string='Status')