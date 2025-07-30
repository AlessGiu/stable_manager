from odoo import http
from odoo.http import request

class FFEConcoursController(http.Controller):

    @http.route('/stable_manager/ffe_concours', type='http', auth='user', website=True)
    def afficher_concours(self, epreuve=None, **kwargs):
        concours = request.env['ffe.concours'].search_concours(epreuve)
        return request.render('stable_manager.template_ffe_concours', {
            'concours': concours,
            'filtre': epreuve or '',
        })
