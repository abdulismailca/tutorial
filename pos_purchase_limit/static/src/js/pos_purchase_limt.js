/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { InfoPopup } from "@pos_purchase_limit/js/popup_component";
import { _t } from "@web/core/l10n/translation";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";

patch(PosStore.prototype, {

    async pay(...args) {
        const order = this.get_order();
        console.log("from settings", order.company_id.name);
        console.log("this ann", this.config.is_activate_purchase_limit_res_settings);

        console.log("Partner undo",order.partner_id)
        const partner = order.partner_id ? order.partner_id : false ;

        const partner_name = partner.name;




        if (!partner) {
            console.log("No partner found!");

            const payload = await makeAwaitable(this.dialog, InfoPopup, {
            title: _t("Please Select a Customer!"),
            heading: _t("Customer Not Selected"),

        });
           return;
        }
        else if(partner){

            if(partner.is_activate_purchase_limit){

                console.log("Purchase limit und");

                if(order.amount_total >= partner.purchase_limit && partner.purchase_limit != 0 ){


                console.log("Purchase limit exceed")
                const payload = await makeAwaitable(this.dialog, InfoPopup, {
                title: _t("Purchase Limit Exceed! "+ partner_name + " Purchase Limit is " +partner.purchase_limit),
                heading:_t("Purchase Limit Exceed"),



        });



                return;

                }else{
                 console.log("No limit exceed.");

                }

            }

        }


        return await super.pay(...args);
    }
});
