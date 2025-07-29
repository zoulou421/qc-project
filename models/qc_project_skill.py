# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class QCTrackerSkillCategory(models.Model):
    _name = 'qcproject.skill.category'
    _description = 'Skill Category'

    name = fields.Char(string='Category Name', required=True, unique=True)


class QCProjectSkill(models.Model):
    _name = 'qcproject.skill'
    _description = 'Employee Skill'

    name = fields.Char(string='Skill Name', required=True, unique=True)
    description = fields.Text(string='Description')
    category_id = fields.Many2one('qcproject.skill.category', string="Category")
    level = fields.Selection([
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ], string='Level')
    last_used = fields.Date(string='Last Used')
    active = fields.Boolean(string='Active', default=True)
    employee_ids = fields.Many2many('qcproject.employee', string="Employees")

    @api.constrains('name')
    def _check_unique_name(self):
        """
        Vérifie si le nom de la compétence est unique.
        Lève une exception ValidationError si le nom de la compétence existe déjà.
        """
        skills = self.search([('name', '=', self.name), ('id', '!=', self.id)])
        if skills:
            raise ValidationError("Skill name must be unique.")