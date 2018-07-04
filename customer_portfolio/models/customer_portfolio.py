
from odoo import api, fields, models


class Portfolio(models.Model):
    _name = 'sale.customer.portfolio'

    name = fields.Char(string='Portfolio name', required=True)
    user_id = fields.Many2one(
        'res.users', string='Salesperson', required=True)
    portfolio_lines = fields.One2many(
        'sale.customer.portfolio.lines', 'portfolio_id', string='Customers')


class PortfolioLines(models.Model):
    _name = 'sale.customer.portfolio.lines'

    portfolio_id = fields.Many2one(
        'sale.customer.portfolio', string='Portfolio', required=True)
    res_partner = fields.Many2one(
        'res.partner', string='Customer', required=True)

    _sql_constraints = [
        ('customer_uniq', 'unique(res_partner)',
         "A client can not belong to more than one portfolio!"),
    ]

    @api.model
    def create(self, vals):
        result = super().create(vals)
        self.env['res.partner'].browse(vals.get('res_partner')).write({
            'user_id': self.env['sale.customer.portfolio'].browse(
                vals.get('portfolio_id')).user_id.id})
        return result

    @api.multi
    def unlink(self):
        for line in self:
            self.env['res.partner'].browse(line.res_partner.id).write({
                'user_id': False})
        return super().unlink()
