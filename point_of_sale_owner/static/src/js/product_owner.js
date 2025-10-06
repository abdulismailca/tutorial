import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline.prototype, {
    setup(vals) {
//        console.log(this.get_product().product_owner.name);
        this.product_owner = this.product_id.product_owner_name || "";
        return super.setup(...arguments);
    },
    getDisplayData() {
//     console.log("helo",this.get_product());
        return {
            ...super.getDisplayData(),

            product_owner: this.get_product().product_owner_name || "",
        };
    },
});


patch(Orderline, {
    props: {
        ...Orderline.props,
        line: {
            ...Orderline.props.line,
            shape: {
                ...Orderline.props.line.shape,
                product_owner: { type: String, optional: true },
            },
        },
    },
});
