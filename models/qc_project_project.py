# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class QCProjectProject(models.Model):
    _name = 'qcproject.project'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'A Project is attached to a Department'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    employee_id = fields.Many2one('qcproject.employee', string='Project Manager')
    task_ids = fields.One2many('qcproject.task', 'project_id', string='Tasks')
    status = fields.Selection([
        ('to_do', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed'),
    ], string='Status', default='to_do', help='Task status')
    project_type = fields.Selection([
        ('internal', 'Internal Project'),
        ('external', 'External Project')
    ], string='Project Type', default='internal', help='Project Type')
    department_id = fields.Many2one('hr.department', string='Department', domain="[('id', 'in', allowed_department_ids)]")
    allowed_department_ids = fields.Many2many(
        'hr.department',
        relation='qcproject_project_allowed_dept_rel',
        column1='project_id',
        column2='department_id',
        string='Allowed Departments',
        help="Sélectionnez un ou plusieurs départements autorisés pour ce projet."
    )
    progress = fields.Integer(string="Progress", compute='_compute_progress', store=True)
    tag_ids = fields.Many2many('qcproject.tag', string="Tags")
    project_delivery_ids = fields.One2many('qcproject.projectdelivery', 'project_id', string='Project Delivery')
    test_department_ids = fields.Many2many(
        'hr.department',
        relation='qcproject_project_test_dept_rel',
        column1='project_id',
        column2='department_id',
        string='Departments',
        domain="[('dpt_type', '=', project_type)]",
        help="Sélectionnez un ou plusieurs départements associés au projet."
    )
    workflow_hierarchy_ids = fields.One2many('workflow.hierarchy', 'project_id', string='Project')

    @api.onchange('project_type')
    def _onchange_project_type(self):
        """
        Réinitialise department_id, allowed_department_ids et test_department_ids, et met à jour les domaines.
        """
        self.department_id = False
        self.allowed_department_ids = [(5, 0, 0)]
        self.test_department_ids = [(5, 0, 0)]
        return {
            'domain': {
                'allowed_department_ids': [('dpt_type', '=', self.project_type)] if self.project_type else [],
                'test_department_ids': [('dpt_type', '=', self.project_type)] if self.project_type else [],
                'department_id': [('id', 'in', self.allowed_department_ids.ids)] if self.allowed_department_ids else [('dpt_type', '=', self.project_type)] if self.project_type else []
            }
        }

    @api.onchange('allowed_department_ids')
    def _onchange_allowed_department_ids(self):
        """
        Met à jour le domaine de department_id et test_department_ids.
        Supprime les départements de test_department_ids qui ne sont plus valides.
        """
        if self.test_department_ids:
            valid_dept_ids = self.allowed_department_ids.ids or self.env['hr.department'].search([('dpt_type', '=', self.project_type)]).ids if self.project_type else []
            self.test_department_ids = [(6, 0, [id for id in self.test_department_ids.ids if id in valid_dept_ids])]
        return {
            'domain': {
                'test_department_ids': [('dpt_type', '=', self.project_type)] if self.project_type else [],
                'department_id': [('id', 'in', self.allowed_department_ids.ids)] if self.allowed_department_ids else [('dpt_type', '=', self.project_type)] if self.project_type else []
            }
        }

    @api.constrains('test_department_ids', 'allowed_department_ids')
    def _check_test_department_ids(self):
        """
        Vérifie que test_department_ids est un sous-ensemble de allowed_department_ids ou des départements autorisés par project_type.
        """
        for record in self:
            if record.allowed_department_ids:
                invalid_depts = record.test_department_ids - record.allowed_department_ids
                if invalid_depts:
                    raise ValidationError("Les départements sélectionnés dans 'Departments' doivent être inclus dans 'Allowed Departments'.")
            else:
                valid_dept_ids = self.env['hr.department'].search([('dpt_type', '=', record.project_type)]).ids if record.project_type else []
                invalid_depts = [dept.id for dept in record.test_department_ids if dept.id not in valid_dept_ids]
                if invalid_depts:
                    raise ValidationError("Les départements sélectionnés dans 'Departments' doivent correspondre au type de projet.")

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        """
        Valide que la date de fin est postérieure à la date de début.
        """
        for record in self:
            if record.start_date and record.end_date and record.end_date < record.start_date:
                raise ValidationError("End date must be after start date.")

    @api.depends('task_ids.status')
    def _compute_progress(self):
        """
        Calcule la progression du projet en fonction des statuts des tâches associées.
        """
        for project in self:
            tasks = project.task_ids
            if tasks:
                completed_tasks = len(tasks.filtered(lambda t: t.status == 'done'))
                project.progress = int((completed_tasks / len(tasks)) * 100)
            else:
                project.progress = 0

    @api.onchange('test_department_ids')
    def _onchange_test_department(self):
        """
        Met à jour workflow_hierarchy_ids en fonction des départements sélectionnés.
        """
        related_workflows = self.env['workflow.hierarchy'].search([
            ('department_id', 'in', self.test_department_ids.ids)
        ])
        self.workflow_hierarchy_ids = [(6, 0, related_workflows.ids)]