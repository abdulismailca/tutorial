/** @odoo-module */
import { Dialog } from "@web/core/dialog/dialog";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Component, useState } from "@odoo/owl";

export class NoResPopup extends Component {
    static template = "pos_purchase_limit.NoResPopup";
    static components = { Dialog };

    setup() {
        this.pos = usePos();
        this.state = useState({});
    }
}
