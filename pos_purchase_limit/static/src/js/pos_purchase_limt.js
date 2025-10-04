/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
//import { NoResPopup } from "@pos_purchase_limit/static/src/js/popup_component";
import { InfoPopup } from "@pos_purchase_limit/js/popup_component";
import { _t } from "@web/core/l10n/translation";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";

patch(PosStore.prototype, {
    async pay(...args) {
        const order = this.get_order();
        console.log("from settings", order.company_id.name);

        console.log("Partner undo",order.partner_id)
        const partner = order.partner_id ? order.partner_id : false ;

//        const partner_name = partner.name;
//        console.log("partner_name", partner_name);
//        console.log("orders res_partnetr", partner.is_activate_purchase_limit)

//        const is_activate_purchase_limit = partner.is_activate_purchase_limit;
//        const purchase_limit = partner.purchase_limit;

//        console.log('this', this)
//        console.log('order', order)
//        console.log("partner", partner);
//        console.log("partner name", partner.parent_name);
//        console.log("partner limit active or not ", partner.is_activate_purchase_limit);
//        console.log("partner limit amount", partner.purchase_limit);
//        console.log("helo there")

        if (!partner) {
            console.log("No partner found!");

            const payload = await makeAwaitable(this.dialog, InfoPopup, {
            title: _t("Please Select a Customer!"),

        });
           return;
        }
        else if(partner){

//        console.log("orders res_partnetr", partner.is_activate_purchase_limit)

            if(partner.is_activate_purchase_limit){

                console.log("Purchase limit und");

                if(order.amount_total >= partner.purchase_limit){

                console.log("Purchase limit exceed")
                const payload = await makeAwaitable(this.dialog, InfoPopup, {
                title: _t("Purchase Limit Exceed! "+ partner_name + " Purchase Limit is " +partner.purchase_limit),



        });



                return;

                }else{
                 console.log("No limit exceed");

                }

            }

        }


        return await super.pay(...args);
    }
});
