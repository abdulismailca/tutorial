/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
//import { NoResPopup } from "@pos_purchase_limit/static/src/js/popup_component";
import { _t } from "@web/core/l10n/translation";

patch(PosStore.prototype, {
    async pay(...args) {
        const order = this.get_order();
        console.log('order', order)
        const partner = order.partner_id;
        const is_activate_purchase_limit = order.partner_id.is_activate_purchase_limit;
        const purchase_limit = order.partner_id.purchase_limit;
        console.log("helo there")

        if (!partner) {
            console.log("No partner found!");
//            await this.dialog.add(NoResPopup, {
//                title: _t("Select Customer"),
//                body: _t("Please select a customer before payment."),
//            });

            return;
        }else{

            if(is_activate_purchase_limit){
                console.log("Purchase limit und");
                if(order.amount_total >= purchase_limit){

                console.log("Purchase limit exceed")
                }else{
                 console.log("No limit exceed");

                }

            }


        }


        return await super.pay(...args);
    }
});
