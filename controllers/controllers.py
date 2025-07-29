# -*- coding: utf-8 -*-
# from odoo import http


# class Qcproject(http.Controller):
#     @http.route('/qcproject/qcproject', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/qcproject/qcproject/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('qcproject.listing', {
#             'root': '/qcproject/qcproject',
#             'objects': http.request.env['qcproject.qcproject'].search([]),
#         })

#     @http.route('/qcproject/qcproject/objects/<model("qcproject.qcproject"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('qcproject.object', {
#             'object': obj
#         })
