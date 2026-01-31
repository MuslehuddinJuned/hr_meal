from odoo import api, models, fields

class MealExpanse(models.Model):
    _name = 'meal.expanse'
    _description = 'Meal Expanse'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    date = fields.Date(string='Date', required=True)
    meal_package_id = fields.Many2one('meal.package', string='Meal Package', required=True)
    amount = fields.Float(string='Amount', compute='_compute_amount', store=True)
    remarks = fields.Text(string='Remarks')
    expanse_line_ids = fields.One2many('meal.expanse.line', 'meal_expanse_id', string='Expanse Lines')


    @api.depends('expanse_line_ids.total_price')
    def _compute_amount(self):
        for rec in self:
            rec.amount = sum(rec.expanse_line_ids.mapped('total_price'))


class MealExpanseLine(models.Model):
    _name = 'meal.expanse.line'
    _description = 'Meal Expanse Line'

    meal_expanse_id = fields.Many2one('meal.expanse', string='Meal Expanse', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    unit = fields.Many2one('uom.uom', string='Unit')
    quantity = fields.Integer(string='Quantity', required=True)
    unit_price = fields.Float(string='Unit Price', required=True)
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_total_price(self):
        for line in self:
            line.total_price = line.quantity * line.unit_price


    @api.onchange('product_id')
    def _onchange_product_id_set_unit(self):
        for line in self:
            if line.product_id:
                line.unit = line.product_id.uom_id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('product_id') and not vals.get('unit'):
                product = self.env['product.product'].browse(vals['product_id'])
                vals['unit'] = product.uom_id.id
        return super().create(vals_list)
