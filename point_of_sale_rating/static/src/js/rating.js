/** @odoo-module */
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";
patch(PosOrder.prototype, {
   export_for_printing() {
       const result = super.export_for_printing(...arguments);
       if (this.props.product.quality_rating) {
           result.headerData.partner = this.props.product.quality_rating;
       }
       return result;
   },
});