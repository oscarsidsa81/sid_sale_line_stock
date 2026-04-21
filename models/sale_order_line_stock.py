from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    sid_qty_stock_mad = fields.Float(
        string="Stock pronosticado (Madrid)",
        compute="_compute_sid_qty_stock_mad",
        store=False,
        readonly=True,
        help="Cantidad pronosticada (virtual_available) en la ubicación de stock del almacén localizado por state_es_m.",
    )

    sid_qty_stock_ptllno = fields.Float(
        string="Stock pronosticado (Ptllno)",
        compute="_compute_sid_qty_stock_ptllno",
        store=False,
        readonly=True,
        help="Cantidad pronosticada (virtual_available) en la ubicación de stock del almacén localizado por state_es_cr.",
    )

    route_first_rule_valued_src = fields.Boolean (
        string="Ruta con primera regla valorada",
        compute="_compute_route_first_rule_valued_src",
        store=True,
    )

    @api.depends (
        'route_id',
        'route_id.rule_ids.sequence',
        'route_id.rule_ids.location_src_id',
        'route_id.rule_ids.location_src_id.is_valued_in_stock',
    )
    def _compute_route_first_rule_valued_src(self) :
        for rec in self :
            value = False
            if rec.route_id and rec.route_id.rule_ids :
                first_rule = rec.route_id.rule_ids.sorted (
                    key=lambda r : r.sequence )[:1]
                value = bool (
                    first_rule and first_rule.location_src_id.is_valued_in_stock )
            rec.route_first_rule_valued_src = value

    def _get_wh_stock_location_by_state_xmlid(self, state_xmlid):
        """Devuelve la lot_stock_id del primer warehouse cuya partner_id.state_id coincida con el state."""
        Warehouse = self.env["stock.warehouse"]
        state = self.env.ref(state_xmlid, raise_if_not_found=False)
        if not state:
            return False

        wh = Warehouse.search([("partner_id.state_id", "=", state.id)], limit=1)
        return wh.lot_stock_id if wh else False

    def _get_virtual_available_in_location(self, product, location):
        if not product or not location:
            return 0.0
        return product.with_context(location=location.id).virtual_available or 0.0

    @api.depends("product_id")
    def _compute_sid_qty_stock_mad(self):
        location = self._get_wh_stock_location_by_state_xmlid("base.state_es_m")
        for line in self:
            line.sid_qty_stock_mad = self._get_virtual_available_in_location(line.product_id, location)

    @api.depends("product_id")
    def _compute_sid_qty_stock_ptllno(self):
        location = self._get_wh_stock_location_by_state_xmlid("base.state_es_cr")
        for line in self:
            line.sid_qty_stock_ptllno = self._get_virtual_available_in_location(line.product_id, location)
