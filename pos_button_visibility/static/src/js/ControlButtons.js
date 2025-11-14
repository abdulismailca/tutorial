/** @odoo-module */
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { useState } from "@odoo/owl";

//Patching ControlButtons
patch(ControlButtons.prototype, {
    async setup(){
        super.setup(...arguments)
        this.state = useState({
            buttons: [],
        })
        let buttons = [];
        if (this.pos.cashier.buttons_pos_ids) {
            var hide_buttons = this.pos.cashier.buttons_pos_ids;
            if (hide_buttons){
                buttons = hide_buttons.map((button) => button.name);
            }
        } else {
            buttons = false;
        }
        this.state.buttons = buttons
    }
})
