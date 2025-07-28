# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class QCProjectTask(models.Model):
    _name = 'qcproject.task'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Add this line
    _description = 'Une tâche appartient à un projet et est assignée à un employé'

    name = fields.Char(string='Nom de la Tâche', required=True)
    description = fields.Text(string='Description de la Tâche')
    process_id = fields.Many2one('qcproject.process', string='Processus')
    sub_process_id = fields.Many2one('qcproject.sub.process', string='Sous-Processus',
                                     domain="[('process_id', '=', process_id)]")
    # employee_id = fields.Many2one('qcproject.employee', string='Employé Assigné')
    employee_id = fields.Many2one('hr.employee', string='Employé Assigné')
    project_id = fields.Many2one('qcproject.project', string='Projet')
    #manager_id = fields.Many2one('qcproject.employee', string='Responsable')
    manager_id = fields.Many2one('hr.employee', string='Responsable')
    start_date = fields.Date(string='Date de Début')
    expected_end_date = fields.Date(string='Date de Fin Prévue')
    end_date = fields.Date(string='Date de Fin Réelle')
    progress = fields.Float(string='Progression', default=0.0, help="Progression de la tâche en pourcentage",
                            digits=(6, 2))
    priority = fields.Selection([('low', 'Basse'), ('medium', 'Moyenne'), ('high', 'Haute')], string='Priorité',
                                default='medium')
    subtask_ids = fields.One2many('qcproject.subtask', 'task_id', string='Sous-Tâches')
    status = fields.Selection([('to_do', 'À Faire'), ('in_progress', 'En Cours'), ('done', 'Terminée')],
                              string='Statut', default='to_do', help='Statut de la tâche')
    note = fields.Text(string='Appreciation')

    workflow_hierarchy_ids = fields.Many2many('workflow.hierarchy', string='Cadres de Références')
    allowed_workflow_hierarchy_ids = fields.Many2many(
        'workflow.hierarchy',
        string='Allowed Cadres de Références',
        compute='_compute_allowed_workflow_hierarchy_ids'
    )
    cadres_link = fields.Char(string='Cadres Link', compute='_compute_cadres_link')

    @api.depends('project_id.workflow_hierarchy_ids')
    def _compute_allowed_workflow_hierarchy_ids(self):
        for task in self:
            task.allowed_workflow_hierarchy_ids = [(6, 0, task.project_id.workflow_hierarchy_ids.ids)]

    @api.depends('workflow_hierarchy_ids')
    def _compute_cadres_link(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        action_id = self.env.ref('qcproject.action_workflow_hierarchy').id
        for task in self:
            if not task.workflow_hierarchy_ids:
                task.cadres_link = ''
            elif len(task.workflow_hierarchy_ids) == 1:
                task.cadres_link = f"{base_url}/web#id={task.workflow_hierarchy_ids.id}&model=workflow.hierarchy&view_type=form&action={action_id}"
            else:
                hierarchy_ids = ','.join(str(id) for id in task.workflow_hierarchy_ids.ids)
                task.cadres_link = f"{base_url}/web#model=workflow.hierarchy&view_type=list&action={action_id}&domain=[('id', 'in', [{hierarchy_ids}])]"

    def action_view_cadres(self):
        self.ensure_one()
        action = self.env.ref('qcproject.action_workflow_hierarchy').read()[0]
        if len(self.workflow_hierarchy_ids) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': self.workflow_hierarchy_ids.id,
                'views': [(False, 'form')],
            })
        else:
            action.update({
                'view_mode': 'tree,form',
                'domain': [('id', 'in', self.workflow_hierarchy_ids.ids)],
            })
        return action

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.end_date < record.start_date:
                raise ValidationError("End date must be after start date.")

    @api.depends('subtask_ids.status')
    def _compute_progress(self):
        for task in self:
            subtasks = task.subtask_ids
            if subtasks:
                completed_subtasks = len(subtasks.filtered(lambda st: st.status == 'done'))
                task.progress = int((completed_subtasks / len(subtasks)) * 100)
            else:
                task.progress = 0
