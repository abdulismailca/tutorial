console.log("helo ismail ")

import { SelectPartnerButton } from "@point_of_sale/app/screens/product_screen/control_buttons/select_partner_button/select_partner_button";
import { patch } from "@web/core/utils/patch";
import {Component} from "@odoo/owl";
import { OrderSummary } from "@point_of_sale/app/screens/product_screen/order_summary/order_summary";
import { ActionpadWidget } from "@point_of_sale/app/screens/product_screen/action_pad/action_pad";

patch(ActionpadWidget.prototype, {
    setup(vals) {
//        console.log('payment button',this.props.partner.name);
        if(!this.props.partner){

         console.log("user not found")


        }else{
         console.log("user found")
         this.onClick();
        }

        return super.setup(...arguments);
    },
    onClick(){

//    console.log(this.props.get_order)
    console.log("function called");
//    console.log(this.props.partner.name);
    }


});


import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Popup } from "@pos_purchase_limit/js/popup";
import { AlertDialog, ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";


patch(PosStore.prototype, {
    async pay() {
        var purchaseLimitEnabled = this.config.customer_purchase_limit
        if (purchaseLimitEnabled) {
            var partner = this.get_order().partner_id;
            if (!partner) {
//                this.dialog.add(AlertDialog, {
//                    title: _t("Customer is required!"),
//                    body: _t("Please provide a customer"),
//                });
                this.dialog.add(Popup, {
                    title: _t("Customer is required!"),
                    body: _t("Please provide a customer"),
                });
                return;
            }

            var customerHasLimit = partner.activate_purchase_limit
            if (customerHasLimit) {
                var limit = partner.purchase_limit_amount;
                var total = this.get_order().getTotalDue();

                if (total > limit && limit != 0) {
                    this.dialog.add(AlertDialog, {
                        title: _t("Oops..."),
                        body: _t(The purchase limit of amount ${limit} has been exceeded for the selected customer ${partner.name}.),
                    });
                    return;
                }
            }
        }
        super.pay();
    }
});

// not important

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { AlertDialog, ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    async validateOrder(isForceValidate) {
        if (!this.currentOrder.get_partner()) {
            this.dialog.add(AlertDialog, {
                title: _t("Customer is required!"),
                body: _t("Please provide a customer"),
            });
            return;
        }

        var customerHasLimit = this.currentOrder.get_partner().activate_purchase_limit
        if (customerHasLimit && this.pos.config.customer_purchase_limit) {
            var limit = this.currentOrder.get_partner().purchase_limit_amount;
            var total = this.currentOrder.getTotalDue();

            if (total > limit && limit != 0) {
                this.dialog.add(AlertDialog, {
                    title: _t("Oops..."),
                    body: _t(The purchase limit of amount ${limit} has been exceeded for the selected customer.),
                });
                return;
            }
        }

        super.validateOrder(isForceValidate);
    }
});
