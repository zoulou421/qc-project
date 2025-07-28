# -*- coding: utf-8 -*-
import re

from stdnum.exceptions import ValidationError

from odoo import models, fields, api


class QCProjectEmployee(models.Model):
    """
       Modèle Odoo représentant un employé.
       Un employé peut appartenir à un département, être un manager et avoir des compétences.
       """
    _name = 'qcproject.employee'
    _description = 'Un employé peut appartenir à un département et être un manager'
    _inherit = ['mail.thread']

    _sql_constraints = [
        ('email_unique', 'UNIQUE(email)', 'L\'adresse e-mail doit être unique.')
    ]

    employee_id = fields.Many2one('hr.employee', string='Employé HR', required=True, ondelete='restrict')
    image_1920 = fields.Binary(string='Profile Image', related='employee_id.image_1920')
    name = fields.Char(string='Nom Complet', related='employee_id.name')
    first_name = fields.Char(string='Prénom', required=True, size=256)
    last_name = fields.Char(string='Nom de Famille', required=True, size=256)
    email = fields.Char(string='Email', related='employee_id.work_email', readonly=True)
    # phone = fields.Char(string='Téléphone', size=32, widget="phone")
    phone = fields.Char(string='Téléphone', related='employee_id.mobile_phone', readonly=True)
    role = fields.Selection([
        ('employee', 'Employé'),
        ('manager', 'Manager'),
        ('admin', 'Administrateur')
    ], string='Rôle', required=True)
    department_id = fields.Many2one('hr.department', string='Département')
    is_manager = fields.Boolean(string='Est Manager', compute='_compute_is_manager', store=True)

    task_ids = fields.One2many('qcproject.task', 'employee_id', string='Tâches Assignées')
    rating_employee_ids = fields.One2many('qcproject.employeerating', 'employee_id', 'Évaluations')
    #gender = fields.Selection([('male', 'Homme'), ('female', 'Femme')], string='Genre')
    gender = fields.Selection(string='Genre', related='employee_id.gender')
    country_id = fields.Many2one('res.country', string='Pays (ID)')
    project_ids = fields.One2many('qcproject.project', 'employee_id', string='Projets')
    user_id = fields.Many2one('res.users', string='Utilisateur Associé')
    project_delivery_ids = fields.One2many('qcproject.projectdelivery', 'employee_id', string='Livraisons de Projet')

    country_dynamic = fields.Selection(
        '_get_country_selection', string='Pays (Dynamique)',
        help='Sélectionnez un pays (liste dynamique)')
    skill_ids = fields.Many2many('qcproject.skill', string='Skills')

    @api.depends('role')
    def _compute_is_manager(self):
        """
        Détermine si l'employé est un manager en fonction de son rôle.
        """
        for rec in self:
            rec.is_manager = rec.role == 'manager'

    @api.model
    def _get_country_selection(self):
        """
        Récupère la liste des pays disponibles pour la sélection dynamique.
        """
        countries = self.env['res.country'].search([])
        return [(str(country.id), country.name) for country in sorted(countries, key=lambda country: country.name)]

    @api.constrains('email')
    def _check_email(self):
        """
        Valide l'adresse e-mail de l'employé en utilisant une expression régulière.
        """
        for record in self:
            if record.email and not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                raise ValidationError("Adresse e-mail invalide.")

    @api.constrains('phone')
    def _check_phone(self):
        """
        Valide le numéro de téléphone de l'employé.
        """
        for record in self:
            if record.phone and not record.phone.isdigit():
                raise ValidationError("Numéro de téléphone invalide. Seuls les chiffres sont autorisés.")
