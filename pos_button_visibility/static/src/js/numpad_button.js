/** @odoo-module */
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { onWillStart } from "@odoo/owl";

/** Patch ProductScreen for override the getNumpadButtons function  **/
patch(ProductScreen.prototype,{
    setup(){
        super.setup()
        this.env.services.pos.user_session = [];
        this.env.services.pos.button = [];
        onWillStart(async () => {
            var session;
                let buttons = [];
                if (this.pos.cashier.buttons_pos_ids) {
                    var hide_buttons = this.pos.cashier.buttons_pos_ids;
                    if (hide_buttons){
                        buttons = hide_buttons.map((button) => button.name);

                    }
                } else {
                    buttons = false;
                }
                this.def = buttons
        })
    },
    getNumpadButtons() {
        if (this.def){
            return [
            { value: "1" },
            { value: "2" },
            { value: "3" },
            { value: "quantity", text: "Qty" },
            { value: "4" },
            { value: "5" },
            { value: "6" },
            { value: "discount", text: "% Disc", disabled: !this.pos.config.manual_discount || this.def.includes('Discount') },
            { value: "7" },
            { value: "8" },
            { value: "9" },
            { value: "price", text: "Price", disabled: !this.pos.cashierHasPriceControlRights() ||this.def.includes('Price') },
            { value: "-", text: "+/-" },
            { value: "0" },
            { value: this.env.services.localization.decimalPoint },
            { value: "Backspace", text: "⌫" },
        ].map((button) => ({
            ...button,
            class: this.pos.numpadMode === button.value ? "active border-primary" : "",
        }));
        }
        else {
        return [
            { value: "1" },
            { value: "2" },
            { value: "3" },
            { value: "quantity", text: "Qty" },
            { value: "4" },
            { value: "5" },
            { value: "6" },
            { value: "discount", text: "% Disc"},
            { value: "7" },
            { value: "8" },
            { value: "9" },
            { value: "price", text: "Price"},
            { value: "-", text: "+/-" },
            { value: "0" },
            { value: this.env.services.localization.decimalPoint },
            { value: "Backspace", text: "⌫" },
        ].map((button) => ({
            ...button,
            class: this.pos.numpadMode === button.value ? "active border-primary" : "",
        }));
        }
    }
});
