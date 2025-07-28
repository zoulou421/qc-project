# --- QCTrackerTag Model ---
from odoo import models, fields


class QCProjectTag(models.Model):
    _name = "qcproject.tag"
    _description = "Project Tags"

    name = fields.Char(string="Tag Name", required=True)