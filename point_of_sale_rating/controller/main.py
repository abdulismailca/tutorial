from odoo import http
from odoo.http import request

class QualityRating(http.Controller):
    @http.route('/quality/rating', auth="public", type='json')
    def get_quality_rating(self):
        records = request.env['product.template'].sudo().search([])
        result = []
        for r in records:
            result.append({
                'id': r.id,
                'quality_rating': r.quality_rating,
            })
        return result


